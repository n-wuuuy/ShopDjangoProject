from rest_framework.routers import SimpleRouter

from client_goods_relation.views import CommentCreateView, LikeCreateView, CommentGoodsView, CommentUserView, \
    LikeUserView, FavoriteCreateView, FavoriteUserView, BasketAddGoodsView, BasketView
from django.urls import path

router = SimpleRouter()
router.register('api/comment', CommentUserView, basename='user_comment')
router.register('api/like', LikeUserView, basename='user_like')
router.register('api/favorite', FavoriteUserView, basename='user_favorite')
router.register('api/basket', BasketView, basename='user_basket')

urlpatterns = [
    path('api/goods/<int:pk>/comment/add/', CommentCreateView.as_view()),
    path('api/goods/<int:pk>/like/add/', LikeCreateView.as_view()),
    path('api/goods/<int:goods_pk>/comment/', CommentGoodsView.as_view()),
    path('api/goods/<int:pk>/favorite/add/', FavoriteCreateView.as_view()),
    path('api/goods/<int:pk>/basket/add/', BasketAddGoodsView.as_view())
]

urlpatterns += router.urls
