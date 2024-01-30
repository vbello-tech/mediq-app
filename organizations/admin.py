from django.contrib import admin
from .models import Organization


# Register your models here.


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organisation_name', 'onboarding_status', 'contact_email_verified', 'access_status', ]
