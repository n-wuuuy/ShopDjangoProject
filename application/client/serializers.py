from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from client.models import Client
from users_app.seralizer import UserSerializer


class ClientSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ('user', 'first_name', 'last_name', 'profile_photo', 'phone_number', 'id')
