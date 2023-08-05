from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from client.models import Client
from client.permissions import IsOwnerOrReadOnly
from client.serializers import ClientSerializer


# Create your views here.

class ClientModelView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Client.objects.all().prefetch_related('user')
    serializer_class = ClientSerializer
    permission_classes = [IsOwnerOrReadOnly]
