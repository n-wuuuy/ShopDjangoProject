from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
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


class RedirectSocial(View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        return JsonResponse(json_obj)
