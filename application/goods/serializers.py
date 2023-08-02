from rest_framework import serializers

from goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True)
    price_with_discount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    category_name = serializers.CharField(read_only=True)
    size = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Goods
        fields = ('name', 'price_with_discount', 'images', 'id', 'likes', 'size',
                  'owner_name', 'is_published', 'category_name', 'company_name', 'time_create',
                  'price', "category")


class GoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('name', 'description', 'price', 'images', 'size', 'discount', 'category', 'company_name')
