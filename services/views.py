
import json

import requests
from environs import Env
from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions, AuthenticationOptions, UniversalAuthMethod

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


env = Env()
env.read_env()

INF_CLIENT_ID=env('INF_CLIENT_ID')
INF_CLIENT_SECRET = env('INF_CLIENT_SECRET')


client = InfisicalClient(
    ClientSettings(
        auth=AuthenticationOptions(
            universal_auth=UniversalAuthMethod(
                client_id=env('INF_CLIENT_ID'),
                client_secret=env('INF_CLIENT_SECRET')
            )
        )
    )
)

def get_inf_secret(secret_name):
    return client.getSecret(
        GetSecretOptions(
            environment=env('INF_ENV'),
            project_id=env('INF_PROJECT_ID'),
            secret_name=secret_name,
        )
    )
# inf_client = InfisicalClient(token=env('INFISICAL_TOKEN'))

NANONETS_OCR_MODEL_ID = get_inf_secret('NANONETS_OCR_MODEL_ID').secret_value
NANONETS_OCR_PREDICT_URL = f"https://app.nanonets.com/api/v2/OCR/Model/{NANONETS_OCR_MODEL_ID}/LabelUrls/"
NANONETS_API_KEY = get_inf_secret('NANONETS_API_KEY').secret_value

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def extract_data_single_image(request):
    request_data = json.loads(request.body)
    image_url = request_data['url']
    print(image_url)
    if not None:
        headers = {
            'accept': 'application/x-www-form-urlencoded'
        }
        data = {
            'urls': [image_url,]
        }

        response = requests.post(
            NANONETS_OCR_PREDICT_URL, 
            auth=requests.auth.HTTPBasicAuth(NANONETS_API_KEY, ''),
            headers=headers,
            data=data
        )
        api_response = response.json()
        print(api_response)
        if api_response['message'] == 'Success':
            predictions = api_response['result'][0]['prediction']
            extract = {}
            for prediction in predictions:
                extract[prediction['label']] = prediction['ocr_text']
            data = {
                'status': 'success',
                'code': 200,
                'message': 'Successful data extraction',
                'data': extract
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'error',
                'code': api_response.get('code', 500),
                'message': 'Data extraction failed',
                'errors': api_response.get('errors', {})
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

