from rest_framework.routers import SimpleRouter

from client_goods_relation.views import CommentCreateView, LikeCreateView, CommentGoodsView, CommentUserView
from django.urls import path

router = SimpleRouter()
router.register('api/comment', CommentUserView, basename='user_comment')

urlpatterns = [
    path('api/goods/<int:pk>/comment/add/', CommentCreateView.as_view()),
    path('api/goods/<int:pk>/like/add/', LikeCreateView.as_view()),
    path('api/goods/<int:goods_pk>/comment/', CommentGoodsView.as_view()),
]

urlpatterns += router.urls
