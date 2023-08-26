from django.conf import settings
from django.db import models

from goods.models import Goods


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    first_name = models.CharField(max_length=64, null=True, default=None, blank=True)
    last_name = models.CharField(max_length=64, null=True, default=None, blank=True)
    profile_photo = models.ImageField(upload_to='user-profile', default='Default_profile.jpg')
    phone_number = models.CharField(max_length=30, null=True, blank=True, default=None)
    newsletter_subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}:({self.first_name} {self.last_name})"
