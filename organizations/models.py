import uuid

from django.db import models

# Create your models here.


class Organization(models.Model):
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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organisation_id = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    organisation_name = models.CharField(max_length=180)
    description = models.TextField(blank=True, null=True)
    onboarding_status = models.CharField(choices=onboarding_chioce, max_length=25)
    organisation_registered = models.BooleanField(default=False)
    organisation_reg_number = models.TextField()
    organisation_email = models.EmailField()
    organisation_phone = models.CharField(max_length=20)
    organisation_website = models.URLField()
    contact_name = models.TextField()
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    contact_email_verified = models.BooleanField(default=False)
    access_status = models.CharField(choices=access_status, max_length=25)

