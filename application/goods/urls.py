from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from goods.views import ShowProducts, ShowDetailProduct

urlpatterns = [
                  path('category/<slug:category_slug>', ShowProducts.as_view(), name='category'),
                  path('<slug:slug>/', ShowDetailProduct.as_view(), name='goods_detail')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
