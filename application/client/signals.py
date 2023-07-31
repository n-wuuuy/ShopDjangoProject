from django.dispatch import receiver
from djoser.signals import user_registered

from client.models import Client


@receiver(user_registered, dispatch_uid="create_client")
def create_client(user, request, **kwargs):
    data = request.data
    Client.objects.create(
        user=user,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        profile_photo=data.get('profile_photo', ''),
        phone_number=data.get('phone_number', '')
    )
