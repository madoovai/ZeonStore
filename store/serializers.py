from rest_framework import serializers
from store.models import Product, Collection, About, News, PublicOffer, ProductImage, Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'rgb')


class ImageSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductImage
        fields = ('image', 'color')


class SimilarProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount', 'size_line', 'collection',
                  'favorite', 'images')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    similar_products = SimilarProductSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'articul', 'discount_price', 'old_price', 'fabric_structure',
            'fabric', 'discount', 'size_line', 'product_amount', 'collection', 'hit', 'latest', 'favorite',
            'images', 'similar_products'
        )


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




