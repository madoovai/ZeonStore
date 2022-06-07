import random

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import ProductLine, Collection, About, News, PublicOffer, Help, ImageHelp, ShoppingCart, Slider, \
    OurAdvantage, \
    Order, OrderItem
from store.pagination import TwelvePagination, EightPagination
from store.serializers import ProductSerializer, CollectionSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer, HelpImageSerializer, CollectionProductSerializer, \
    FavoriteProductSerializer, SliderSerializer, HitSaleProductsSerializer, \
    LatestProductsSerializer, OurAdvantagesSerializer, OrderSerializer, ShoppingCartSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductLine.objects.all()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    # viewset для Корзины
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    """
    - Клонирование объектов Корзины в OrderItem при создании объекта Заказа
    - order.calculate_order_data() - Общий расчет цен, колво линеек и продуктов Заказа
    - ShoppingCart.objects.all().delete() - Опустошение корзины
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        order = serializer.save()

        for item in ShoppingCart.objects.all():
            OrderItem.objects.create(title=item.title, color=item.color, image=item.image,
                                     total_old_price=item.total_old_price, order=order,
                                     total_discount_price=item.total_discount_price, size_line=item.size_line,
                                     amount_of_productline=item.amount_of_productline, product=item.product)
        order.calculate_order_data()

        ShoppingCart.objects.all().delete()


def random_products():
    """
    метод для 5 рандомных товаров
    """
    products = ProductLine.objects.all()
    random_products = random.sample(list(products), 5)
    return random_products


class FavoriteProductViewSet(viewsets.ModelViewSet):
    """
    отображение Избранных товаров в API с проверкой если товаров в Избранном нет,
    то вызывается метод для рандомных товаров (метод находится выше)
    + пагинация 12
    """
    queryset = ProductLine.objects.filter(favorite=True)
    serializer_class = FavoriteProductSerializer
    pagination_class = TwelvePagination

    def get_queryset(self):
        queryset = ProductLine.objects.filter(favorite=True)
        if len(queryset) == 0:
            return random_products()
        else:
            return queryset



class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    pagination_class = EightPagination

    @action(detail=True, methods=['get'], url_path='products')
    def get_products_of_collection(self, request, pk):
        """
        декоратор для отображения отфильтрованных по коллекции продуктов в API + пагинация
        """
        products = ProductLine.objects.filter(collection=pk)
        paginator = TwelvePagination()
        page = paginator.paginate_queryset(products, request)
        serializer = CollectionProductSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'], url_path='latest-products')
    def get_latest_products_of_collection(self, request, pk):
        """
        декоратор для отображения отфильтрованных по коллекции продуктов со статусом "Новинка" в API + пагинация
        """
        latest_products = ProductLine.objects.filter(collection=pk, latest=True)
        serializer = CollectionProductSerializer(latest_products, many=True)
        return Response(serializer.data)


class AboutUsViewSet(viewsets.ModelViewSet):

    serializer_class = AboutUsSerializer
    queryset = About.objects.all()


class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = NewsSerializer
    queryset = News.objects.all()


class PublicOfferViewSet(viewsets.ModelViewSet):

    serializer_class = PublicOfferSerializer
    queryset = PublicOffer.objects.all()


class HelpViewSet(viewsets.ModelViewSet):

    serializer_class = HelpSerializer
    queryset = Help.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        help_image = ImageHelp.objects.all().first()
        if help_image:
            image_serializer = HelpImageSerializer(instance=help_image)
            response.data["image"] = image_serializer.data
        return response


class SliderViewSet(viewsets.ModelViewSet):

    serializer_class = SliderSerializer
    queryset = Slider.objects.all()


class HitSaleProductsViewSet(viewsets.ModelViewSet):
    serializer_class = HitSaleProductsSerializer
    queryset = ProductLine.objects.filter(hit=True)
    pagination_class = EightPagination


class LatestProductsViewSet(viewsets.ModelViewSet):
    serializer_class = LatestProductsSerializer
    queryset = ProductLine.objects.filter(latest=True)
    pagination_class = EightPagination


class OurAdvantagesViewSet(viewsets.ModelViewSet):

    serializer_class = OurAdvantagesSerializer
    queryset = OurAdvantage.objects.all()




