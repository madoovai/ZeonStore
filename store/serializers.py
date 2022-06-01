from rest_framework import serializers
from store.models import Product, Collection, About, News, PublicOffer, ProductImage, Color, AboutImage, ImageHelp, \
    Help, Bag


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'rgb')


class ImageSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductImage
        fields = ('image', 'color')


class CollectionProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount', 'size_line',
                  'favorite', 'images', 'colors')


class SimilarProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount', 'size_line', 'collection',
                  'favorite', 'images')


class FavoriteProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount', 'size_line',
                  'favorite', 'images', 'colors')
        #сериализатор для избранных товаров


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)
    similar_products = SimilarProductSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'articul', 'discount_price', 'old_price', 'fabric_structure',
            'fabric', 'discount', 'size_line', 'product_amount', 'collection', 'hit', 'latest', 'favorite', 'colors',
            'images', 'similar_products'
        )


class BagProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bag
        fields = ('id', 'product_id', 'amount_of_product', 'color_id', 'title',
                  'size_line', 'old_price', 'discount_price')
#сериалайзер для Корзины


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ('id', 'title', 'image')


class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ('image')


class AboutUsSerializer(serializers.ModelSerializer):
    images = AboutImageSerializer(many=True)

    class Meta:
        model = About
        fields = ('headline', 'description', 'images')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('headline', 'description', 'photo')


class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('headline', 'description')


class HelpImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHelp
        fields = ('__all__')


class HelpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Help
        fields = ('id', 'question', 'answer')



