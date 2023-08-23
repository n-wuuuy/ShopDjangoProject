from rest_framework.routers import SimpleRouter
from django.urls import path

from client.views import ClientModelView
from goods.views import GoodsModelView, CategoryModelView, SizeModelView, GoodsCreateModelView, CommentCreateView

urlpatterns = [
    path('api/goods/create', GoodsCreateModelView.as_view()),
    path('api/comment/create', CommentCreateView.as_view()),
]

router = SimpleRouter()
router.register('api/goods', GoodsModelView)
router.register('api/category', CategoryModelView)
router.register('api/size', SizeModelView)
router.register('api/client', ClientModelView)
urlpatterns += router.urls
