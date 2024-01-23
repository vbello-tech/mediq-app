
import uuid

from django.db import models

class Account(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_id = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.TextField()
    phone = models.TextField()
    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    organisation = models.TextField()
    organisation_role = models.TextField()
    onboarding_status = models.TextField()
