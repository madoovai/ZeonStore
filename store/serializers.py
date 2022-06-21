from rest_framework import serializers
from store.models import ProductLine, Collection, About, News, PublicOffer, \
                         ProductImage, Color, AboutImage, ImageHelp, Help, \
                         ShoppingCart, Slider, Order, OurAdvantage, Footer, \
                         SecondFooter, CallBack, OrderItem


class ColorSerializer(serializers.ModelSerializer):
    """сериализатор для Цветов Изображений"""
    class Meta:
        model = Color
        fields = ('name', 'rgb')


class ImageSerializer(serializers.ModelSerializer):
    """сериализатор для Изображений Продукта"""
    color = ColorSerializer()

    class Meta:
        model = ProductImage
        fields = ('image', 'color')


class CollectionProductSerializer(serializers.ModelSerializer):
    """сериализатор для Коллекция(Товары)"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount',
                  'size_line', 'favorite', 'images', 'colors')


class SimilarProductSerializer(serializers.ModelSerializer):
    """сериализатор для Похожих товары"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount',
                  'size_line', 'collection', 'favorite', 'colors', 'images')


class FavoriteProductSerializer(serializers.ModelSerializer):
    """сериализатор для Избранных товаров"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount',
                  'size_line', 'favorite', 'images', 'colors')


class ProductSerializer(serializers.ModelSerializer):
    """сериализатор для Товаров + Похожие товары"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)
    similar_products = SimilarProductSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'id', 'title', 'articul', 'discount_price', 'old_price',
            'fabric_structure', 'fabric', 'discount', 'size_line',
            'product_amount', 'collection', 'hit', 'latest', 'favorite',
            'colors', 'images', 'similar_products'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """сериалайзер для Корзины"""
    class Meta:
        model = ShoppingCart
        fields = ('id', 'product', 'amount_of_productline', 'color', 'title',
                  'size_line', 'old_price', 'discount_price', 'image')


class OrderItemsSerializer(serializers.ModelSerializer):
    """
    сериалайзер для Товаров оформленного заказа
    """
    class Meta:
        model = OrderItem
        fields = ('product', 'amount_of_productline', 'color', 'title',
                  'size_line', 'old_price', 'discount_price', 'image')


class OrderSerializer(serializers.ModelSerializer):
    """
    API заказа, вся информация о заказе(пользователь, инфо о заказе и продукты)
    на одной странице
    """
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'last_name', 'email', 'phone_number',
                  'country', 'city', 'order_date', 'order_status',
                  'amount_of_productlines', 'total_number_of_products',
                  'total_price_without_discount', 'total_discount',
                  'final_total_price', 'order_items')


class CollectionSerializer(serializers.ModelSerializer):
    """сериализатор для Коллекции"""
    class Meta:
        model = Collection
        fields = ('id', 'title', 'image')


class AboutImageSerializer(serializers.ModelSerializer):
    """сериализатор для Изображений для О нас"""
    class Meta:
        model = AboutImage
        fields = ('image',)


class AboutUsSerializer(serializers.ModelSerializer):
    """сериализатор для О нас"""
    images = AboutImageSerializer(many=True)

    class Meta:
        model = About
        fields = ('headline', 'description', 'images')


class NewsSerializer(serializers.ModelSerializer):
    """сериализатор для Новости"""
    class Meta:
        model = News
        fields = ('headline', 'description', 'photo')


class PublicOfferSerializer(serializers.ModelSerializer):
    """сериализатор для Публичной офферты"""
    class Meta:
        model = PublicOffer
        fields = ('headline', 'description')


class HelpImageSerializer(serializers.ModelSerializer):
    """сериализатор для Изображения для Помощь"""
    class Meta:
        model = ImageHelp
        fields = ('__all__',)


class HelpSerializer(serializers.ModelSerializer):
    """сериализатор для Помощь"""
    class Meta:
        model = Help
        fields = ('id', 'question', 'answer')


class SliderSerializer(serializers.ModelSerializer):
    """сериализатор для Слайдер"""
    class Meta:
        model = Slider
        fields = ('photo', 'link')


class HitSaleProductsSerializer(serializers.ModelSerializer):
    """сериализатор для Хит продаж"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price',
                  'discount', 'size_line', 'favorite', 'images', 'colors')


class LatestProductsSerializer(serializers.ModelSerializer):
    """сериализатор для Товаров со статусом Новинка"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount',
                  'size_line', 'favorite', 'images', 'colors')


class OurAdvantagesSerializer(serializers.ModelSerializer):
    """сериализатор для Наши преимущества"""
    class Meta:
        model = OurAdvantage
        fields = ('icon', 'headline', 'description')


class SecondFooterSerializer(serializers.ModelSerializer):
    """Сериализатор для Второй вкладки Футера"""
    class Meta:
        model = SecondFooter
        fields = ('type', 'input_field')


class FooterSerializer(serializers.ModelSerializer):
    """Сериализатор для первой вкладки Футера"""
    numbers_and_social_media = SecondFooterSerializer(many=True)

    class Meta:
        model = Footer
        fields = ('phone_number', 'logotype', 'text_info',
                  'numbers_and_social_media')


class CallBackSerializer(serializers.ModelSerializer):
    """Сериализатор для Обратного звонка"""
    class Meta:
        model = CallBack
        fields = ('name', 'phone_number', 'callback_type')


class SearchProductSerializer(serializers.ModelSerializer):
    """Сериализатор для поиска товаров"""
    images = ImageSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ('id', 'title', 'discount_price', 'old_price', 'discount',
                  'size_line', 'favorite', 'colors', 'images')

