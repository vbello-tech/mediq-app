import random, string
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework import status


# generate random 5 digits that would be used as organisation_id.
def code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    create organisation
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organisation_registered=True, organisation_id=code())
        return super().perform_create(serializer)

    def perform_destroy(self, serializer):
        return super().perform_destroy(serializer)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_organisation(request, uuid):
    """fetch organisation with a specific uuid """
    business = Organization.objects.get(uuid=uuid)
    serializer = OrganizationSerializer(business, many=False)
    if serializer:
        return Response({
            'name': serializer.data,
        })


class VerifyOrganisationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid, *args, **kwargs):
        organisation = get_object_or_404(Organization, uuid=uuid)
        organisation.onboarding_status = 'onboarding_complete'
        organisation.access_status = 'access_granted'
        organisation.save()
        data = {
            "organisation_name": organisation.organisation_name,
            "organisation_id": organisation.organisation_id,
            "onboarding_status": organisation.onboarding_status,
            "access_status": organisation.access_status,
        }
        return Response(
            {
                "message": "Your organisation has been verified",
                "data": data,
                "status": "success"
            }, status=status.HTTP_200_OK)


class VerifyContactPersonView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid, *args, **kwargs):
        organisation = get_object_or_404(Organization, uuid=uuid)
        organisation.contact_email_verfied = True
        organisation.save()
        data = {
            "organisation_contact_name": organisation.contact_name,
            "organisation_contact_phone": organisation.contact_phone,
            "organisation_contact_email": organisation.contact_email,
            "organisation_contact_email_verified": organisation.contact_email_verfied,
        }
        return Response(
            {
                "message": "Your organisation contact person has been verified has been verified",
                "data": data,
                "status": "success"
            }, status=status.HTTP_200_OK)