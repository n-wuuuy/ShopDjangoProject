from django.db.models import Count, Case, F, When, Prefetch
from djoser.conf import User
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from goods.models import Goods, GoodsCategory, GoodsSize, Comment
from goods.permissions import IsOwnerOrStaffOrReadOnly
from goods.serializers import GoodsListSerializer, GoodsCreateSerializer, CategorySerializer, SizeSerializer, \
    GoodsDitailSerializer
from goods.viewsets import NotCreateViewSet


class GoodsModelView(NotCreateViewSet):
    queryset = Goods.objects.all().annotate(likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
                                            price_with_discount=(F('price') -
                                                                 F('price') *
                                                                 F('discount') / 100),
                                            ).order_by('time_create').select_related('category').prefetch_related(
        Prefetch('owner', queryset=User.objects.all().select_related('user').only('username')),
        'comment')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'owner_name', 'category', 'company_name']
    ordering_fields = ['price_with_discount', 'name', 'likes', 'time_create']
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return GoodsListSerializer
        else:
            return GoodsDitailSerializer


class GoodsCreateModelView(ListCreateAPIView):
    queryset = Goods.objects.all().order_by('time_create').prefetch_related('size')
    serializer_class = GoodsCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryModelView(ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.all().order_by('name').prefetch_related('category_goods')
    serializer_class = CategorySerializer


class SizeModelView(ReadOnlyModelViewSet):
    queryset = GoodsSize.objects.all().order_by('size_name').prefetch_related('size_goods__category')
    serializer_class = SizeSerializer
