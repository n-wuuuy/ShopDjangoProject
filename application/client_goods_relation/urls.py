from rest_framework.routers import SimpleRouter

from client_goods_relation.views import CommentCreateView, LikeCreateView
from django.urls import path


urlpatterns = [
    path('api/goods/<int:pk>/comment/add/', CommentCreateView.as_view()),
    path('api/goods/<int:pk>/like/add/', LikeCreateView.as_view()),
]
