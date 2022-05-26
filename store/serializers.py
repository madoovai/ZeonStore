from rest_framework import serializers
from store.models import Product, Collection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'articul', 'discount_price', 'old_price', 'old_price', 'fabric_structure',
                  'fabric', 'discount', 'size_line', 'product_amount', 'collection', 'hit', 'latest', 'favorite')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'image')
