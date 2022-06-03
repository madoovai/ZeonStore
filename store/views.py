import random

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import Product, Collection, About, News, PublicOffer, Help, ImageHelp, Bag, Slider, OurAdvantage, \
    Order
from store.pagination import TwelvePagination
from store.serializers import ProductSerializer, CollectionSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer, HelpImageSerializer, CollectionProductSerializer, \
    FavoriteProductSerializer, BagProductsSerializer, SliderSerializer, HitSaleProductsSerializer, \
    LatestProductsSerializer, OurAdvantagesSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BagProductViewSet(viewsets.ModelViewSet):

    serializer_class = BagProductsSerializer
    queryset = Bag.objects.all()
#viewset для Корзины


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


def random_products():
    products = Product.objects.all()
    random_products = random.sample(list(products), 5)
    return random_products
#метод для 5 рандомных товаров


class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(favorite=True)
    serializer_class = FavoriteProductSerializer
    pagination_class = TwelvePagination

    def get_queryset(self):
        queryset = Product.objects.filter(favorite=True)
        if len(queryset) == 0:
            return random_products()
        else:
            return queryset
    #viewset для отображения Избранных товаров в API с проверкой если товаров в Избранном нет,
    #то вызывается метод для рандомных товаров (метод находится выше)
    # + пагинация 12


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    @action(detail=True, methods=['get'], url_path='products')
    def get_products_of_collection(self, request, pk):
        products = Product.objects.filter(collection=pk)
        paginator = TwelvePagination()
        page = paginator.paginate_queryset(products, request)
        serializer = CollectionProductSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    #декоратор для отображения отфильтрованных по коллекции продуктов в API + пагинация

    @action(detail=True, methods=['get'], url_path='latest-products')
    def get_latest_products_of_collection(self, request, pk):
        latest_products = Product.objects.filter(collection=pk, latest=True)
        serializer = CollectionProductSerializer(latest_products, many=True)
        return Response(serializer.data)
    #декоратор для отображения отфильтрованных по коллекции и статусу "Новинка" продуктов в API


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
    queryset = Product.objects.all()


class LatestProductsViewSet(viewsets.ModelViewSet):

    serializer_class = LatestProductsSerializer
    queryset = Product.objects.all()


class OurAdvantagesViewSet(viewsets.ModelViewSet):

    serializer_class = OurAdvantagesSerializer
    queryset = OurAdvantage.objects.all()


# class MainPageApiViewSet(viewsets.ModelViewSet):
#     pass

    # serializer_class = [SliderSerializer, HitSaleProductsSerializer, LatestProductsViewSet,
    #                     CollectionSerializer, OurAdvantagesSerializer]




