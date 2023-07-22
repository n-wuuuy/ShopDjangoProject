from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet

from goods.models import Goods
from goods.serializers import GoodsSerializer


class GoodsModelView(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class ShowProducts(ListView):
    model = Goods
    template_name = 'goods/products.html'
    allow_empty = False

    def get_queryset(self):
        return Goods.objects.filter(category__slug=self.kwargs['category_slug'])
