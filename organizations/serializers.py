from rest_framework import serializers

from .models import Organization


class OrganizationSerializer(serializers.Serializer):
    onboarding_chioce = [
        ('onboarding_incomplete', 'onboarding_incomplete'),
        ('verification_pending', 'verification_pending'),
        ('verification_queried', 'verification_queried'),
        ('onboarding_complete', 'onboarding_complete')
    ]

    access_status = [
        ('access_granted', 'access_granted'),
        ('access_suspended', 'access_suspended'),
        ('access_banned', 'access_banned'),
    ]

    uuid = serializers.CharField(read_only=True)
    organisation_id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
    organisation_name = serializers.CharField(required=True, allow_blank=False)
    description = serializers.CharField()
    onboarding_status = serializers.ChoiceField(choices=onboarding_chioce, read_only=True)
    organisation_registered = serializers.BooleanField(default=False, read_only=True)
    organisation_reg_number = serializers.CharField()
    organisation_email = serializers.EmailField()
    organisation_phone = serializers.CharField()
    organisation_website = serializers.URLField()
    contact_name = serializers.CharField(required=True, allow_blank=False)
    contact_phone = serializers.CharField()
    contact_email = serializers.EmailField()
    contact_email_verified = serializers.CharField()
    access_status = serializers.ChoiceField(choices=access_status, read_only=True)

    def create(self, validated_data):
        """
        Create and return a new Account
        """

        return Organization.objects.create(**validated_data)


