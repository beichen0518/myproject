import django_filters
from rest_framework import filters

from ai_func.models import Goods, CartModel


class GoodsFilter(filters.FilterSet):
    pass

    class Meta:
        model = Goods
        fields = []


class CartFilter(filters.FilterSet):
    id = django_filters.CharFilter('id')
    userid = django_filters.CharFilter('user_id')
    goodid = django_filters.CharFilter('goods_id')
    count = django_filters.CharFilter('c_num')
    status = django_filters.CharFilter('is_select')

    class Meta:
        model = CartModel
        fields = []