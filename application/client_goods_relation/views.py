from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from client_goods_relation.models import Comment, Like, InFavorites, Basket
from client_goods_relation.serializers import CommentCreateSerializer, LikeCreateSerializer, CommentGoodsSerializer, \
    CommentUserSerializer, LikeUserSerializer, FavoriteCreateSerializer, FavoriteUserSerializer, \
    BasketAddGoodsSerializer, BasketSerializers
from goods.models import Goods
from goods.permissions import IsOwnerOrStaffOrReadOnly
from goods.viewsets import NotCreateViewSet


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
        serializer.save(owner=self.request.user)


class CommentGoodsView(ListAPIView):
    serializer_class = CommentGoodsSerializer

    def get_queryset(self):
        goods = Goods.objects.get(id=self.kwargs['goods_pk'])
        return Comment.objects.filter(goods=goods)


class CommentUserView(NotCreateViewSet):
    serializer_class = CommentUserSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        goods = Goods.objects.get(id=self.kwargs.get('pk'))
        serializer.validated_data['goods'] = goods
        serializer.save(owner=self.request.user)


class LikeUserView(NotCreateViewSet):
    serializer_class = LikeUserSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        return Like.objects.filter(owner=self.request.user)


class FavoriteCreateView(CreateAPIView):
    queryset = InFavorites.objects.all()
    serializer_class = FavoriteCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        goods = Goods.objects.get(id=self.kwargs.get('pk'))
        serializer.validated_data['goods'] = goods
        serializer.save(owner=self.request.user)


class FavoriteUserView(NotCreateViewSet):
    serializer_class = FavoriteUserSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        return InFavorites.objects.filter(owner=self.request.user)


class BasketAddGoodsView(CreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketAddGoodsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        goods = Goods.objects.get(id=self.kwargs.get('pk'))
        serializer.validated_data['goods'] = goods
        serializer.save(owner=self.request.user)


class BasketView(NotCreateViewSet):
    serializer_class = BasketSerializers
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        return Basket.objects.filter(owner=self.request.user)
