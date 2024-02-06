import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Organization
from .serializers import OrganizationSerializer


# generate random 5 digits that would be used as organisation_id.
def code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


class OrganizationCreateAndFetchAll(GenericAPIView):
    """
    view to creating organisation and fetching all organisations
    post request to create
    get request to fetch
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        """Retrieve"""
        organisation = Organization.objects.all()
        serializer = self.serializer_class(organisation, many=True)
        if serializer:
            return Response({
                'message': 'All Organizations details fetched',
                'data': serializer.data,
                'status': 'success'
            }, status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        created_organization = serializer.save()
        serialized_data = self.serializer_class(created_organization).data

        return Response(
            {
                "message": "Organization created successfully",
                "data": serialized_data,
                "status": "success"
            }, status=status.HTTP_201_CREATED)


class OrganizationRetrieveUpdateDeleteView(GenericAPIView):
    """
    View to handle fetching, updating and deleting an organization
    """
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        """Retrieve"""
        try:
            organisation = Organization.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({
                "message": "Organization does not exist",
                "status": "failed"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationSerializer(organisation, many=False)
        if serializer:
            return Response({
                'message': 'Organization details fetched',
                'data': serializer.data,
                'status': 'success'
            }, status.HTTP_200_OK)

    def patch(self, request, uuid, *args, **kwargs):
        """Update"""
        try:
            organisation = Organization.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({
                "message": "You dont have an Organization",
                "status": "failed"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(organisation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        saved_serializer = serializer.save()
        serialized_data = OrganizationSerializer(saved_serializer).data
        return Response(
            {
                "message": "Organization updated",
                "data": serialized_data,
                "status": "success"
            }, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, uuid, *args, **kwargs):
        """Delete"""
        try:
            organisation = Organization.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({
                "message": "Organization Does not exist",
                "status": "failed"
            }, status=status.HTTP_404_NOT_FOUND)
        organisation.delete()
        return Response({
            "message": "Organization deleted",
            "status": "sucess"
        }, status=status.HTTP_204_NO_CONTENT)


class VerifyOrganisationView(GenericAPIView):
    """
    view to handle verifying an organisation
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid, *args, **kwargs):
        try:
            organisation = get_object_or_404(Organization, uuid=uuid)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "Your organisation verification failed",
                    "status": "Organization not found"
                }, status=status.HTTP_404_NOT_FOUND)
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
    """
    view to handle verifying an organization contact person
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid, *args, **kwargs):
        try:
            organisation = get_object_or_404(Organization, uuid=uuid)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "Your organisation contact person verification failed",
                    "status": "Organization not found"
                }, status=status.HTTP_404_NOT_FOUND)
        organisation.contact_email_verified = True
        organisation.save()
        data = {
            "organisation_contact_name": organisation.contact_name,
            "organisation_contact_phone": organisation.contact_phone,
            "organisation_contact_email": organisation.contact_email,
            "organisation_contact_email_verified": organisation.contact_email_verified,
        }
        return Response(
            {
                "message": "Your organisation contact person has been verified has been verified",
                "data": data,
                "status": "success"
            }, status=status.HTTP_200_OK)
