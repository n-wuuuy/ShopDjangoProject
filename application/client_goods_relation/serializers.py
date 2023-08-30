from rest_framework import serializers

from client_goods_relation.models import Comment, Like, InFavorites


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("owner", 'goods')


class CommentGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('goods',)


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ("owner", 'goods')

    def create(self, validated_data):
        like, _ = Like.objects.update_or_create(
            owner=validated_data.get('owner', None),
            goods=validated_data.get('goods', None),
            defaults={'like': validated_data.get("like", None)}
        )
        return like


class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InFavorites
        exclude = ("owner", 'goods')

    def create(self, validated_data):
        favorite, _ = InFavorites.objects.update_or_create(
            owner=validated_data.get('owner', None),
            goods=validated_data.get('goods', None),
            defaults={'favorite': validated_data.get("favorite", None)}
        )
        return favorite


class FavoriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InFavorites
        fields = '__all__'
