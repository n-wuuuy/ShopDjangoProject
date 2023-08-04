from django.db.models import Count, Case, F, When
from django.views.generic import ListView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from goods.models import Goods, GoodsCategory, GoodsSize
from goods.permissions import IsOwnerOrStaffOrReadOnly
from goods.serializers import GoodsSerializer, GoodsCreateSerializer, CategorySerializer, SizeSerializer
from goods.viewsets import NotCreateViewSet


class GoodsModelView(NotCreateViewSet):
    queryset = Goods.objects.all().annotate(likes=Count(Case(When(clientgoodsrelation__like=True, then=1))),
                                            owner_name=F('owner__username'),
                                            price_with_discount=(F('price') -
                                                                 F('price') *
                                                                 F('discount') / 100),
                                            # category_name=F('category__name')
                                            ).order_by('time_create').prefetch_related('size').select_related(
        'category')
    serializer_class = GoodsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'owner_name', 'category', 'company_name']
    ordering_fields = ['price_with_discount', 'name', 'likes', 'time_create']
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class GoodsCreateModelView(ListCreateAPIView):
    queryset = Goods.objects.all().order_by('time_create').prefetch_related('size')
    serializer_class = GoodsCreateSerializer
    permission_classes = [IsAuthenticated]

    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'homepage.html'

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryModelView(ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.all().order_by('name').prefetch_related('category_goods').prefetch_related('category_goods__size')
    serializer_class = CategorySerializer


class SizeModelView(ReadOnlyModelViewSet):
    queryset = GoodsSize.objects.all().order_by('size_name').prefetch_related('size_goods__category').prefetch_related('size_goods__size')
    serializer_class = SizeSerializer


class ShowProducts(ListView):
    model = Goods
    template_name = 'goods/products.html'
    allow_empty = False

    def get_queryset(self):
        return Goods.objects.filter(category__slug=self.kwargs['category_slug'])
