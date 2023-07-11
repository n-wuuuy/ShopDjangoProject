from rest_framework import serializers

from goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goods
        fields = '__all__'
