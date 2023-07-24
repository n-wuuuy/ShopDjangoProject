from django.db.models import Count, Case, F
from django.views.generic import ListView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from goods.models import Goods
from goods.serializers import GoodsFilteredByCategorySerializer


class GoodsModelView(ModelViewSet):
    queryset = Goods.objects.all().annotate(likes=Count(Case(clientgoodsrelation__like=True, then=1)),
                                            owner_name=F('owner__username'),
                                            price_with_discount=(F('price') -
                                                                 F('price') *
                                                                 F('discount') / 100),
                                            category_name=F('category__name')
                                            )
    serializer_class = GoodsFilteredByCategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'owner_name', 'category__name', 'company_name']
    ordering_fields = ['price_with_discount', 'name', 'likes', 'time_create']


class ShowProducts(ListView):
    model = Goods
    template_name = 'goods/products.html'
    allow_empty = False

    def get_queryset(self):
        return Goods.objects.filter(category__slug=self.kwargs['category_slug'])
