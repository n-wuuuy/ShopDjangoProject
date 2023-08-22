from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsSize, GoodsImages, Comment


class GoodsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImages
        fields = ('image',)


class GoodsListSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    price_with_discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Goods
        fields = ('name', 'price_with_discount', 'images', 'id', 'likes',
                  'is_published', 'company_name', 'time_create',
                  'price', "category")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "owner", "text")


class GoodsDitailSerializer(serializers.ModelSerializer):
    goods_images = GoodsImagesSerializer(many=True, read_only=True)
    size = serializers.StringRelatedField(read_only=True, many=True)
    price_with_discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    owner_name = serializers.CharField(source='owner.username')
    likes = serializers.IntegerField(read_only=True)
    comment = CommentSerializer(many=True)

    class Meta:
        model = Goods
        fields = ('name', 'description', 'price', 'discount', 'price_with_discount', 'images',
                  'goods_images', 'size', 'comment', 'is_published', 'owner_name', 'company_name', 'likes')


class GoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('name', 'description', 'price', 'images', 'size', 'discount', 'category', 'company_name')


class CategorySerializer(serializers.ModelSerializer):
    category_goods = GoodsListSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ('name', 'category_goods')


class SizeSerializer(serializers.ModelSerializer):
    size_goods = GoodsListSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsSize
        fields = ('size_name', 'size_value', 'size_goods')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("owner",)
