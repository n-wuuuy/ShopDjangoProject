from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from client_goods_relation.models import Comment, Like
from client_goods_relation.serializers import CommentCreateSerializer, LikeCreateSerializer, CommentSerializer
from goods.models import Goods


# Create your views here.
class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        goods = Goods.objects.get(id=self.kwargs.get('pk'))
        serializer.validated_data['goods'] = goods
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request,):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        goods = Goods.objects.get(id=self.kwargs.get('pk'))
        serializer.validated_data['goods'] = goods
        serializer.save(owner=self.request.user)
