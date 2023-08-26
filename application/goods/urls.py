from rest_framework.routers import SimpleRouter
from django.urls import path

from goods.views import GoodsModelView, CategoryModelView, SizeModelView, GoodsCreateModelView

urlpatterns = [
    path('api/goods/create', GoodsCreateModelView.as_view()),
]

router = SimpleRouter()
router.register('api/goods', GoodsModelView)
router.register('api/category', CategoryModelView)
router.register('api/size', SizeModelView)
urlpatterns += router.urls
