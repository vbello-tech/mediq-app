from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Account


@receiver(post_save, sender=Account)
def user_token(sender, instance, created, request, *args, **kwargs):
    if created:
        Token.objects.create(user=request.user)

