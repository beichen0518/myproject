from rest_framework import serializers
from ai_func.models import Goods, CartModel


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ['id']

    def to_representation(self, instance):

        data = super().to_representation(instance)
        return data


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['id', 'goods_id', 'user_id', 'c_num', 'is_select']
        depth = 1

    def to_representation(self, instance):

        data = super().to_representation(instance)
        return data