from rest_framework import serializers
from store.models import Product, Collection, About, News, PublicOffer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'articul', 'discount_price', 'old_price', 'fabric_structure',
                  'fabric', 'discount', 'size_line', 'product_amount', 'collection', 'hit', 'latest', 'favorite')


class SimilarProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount', 'size_line', 'collection', 'favorite')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'image')


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('headline', 'description', 'image')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('headline', 'description', 'photo')


class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('headline', 'description')


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('question', 'answer')




