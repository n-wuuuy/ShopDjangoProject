from rest_framework import serializers

from client_goods_relation.models import Comment, Like


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
