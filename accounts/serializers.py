
from rest_framework import serializers

from accounts.models import Account

class AccountSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    account_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField()
    email = serializers.EmailField()
    email_verified = serializers.BooleanField(read_only=True)
    password = serializers.CharField()
    organisation = serializers.CharField()
    organisation_role = serializers.CharField()
    onboarding_status = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new Account
        """

        return Account.objects.create(**validated_data)
    