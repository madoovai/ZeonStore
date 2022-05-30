from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import Product, Collection, About, News, PublicOffer, Help, ImageHelp
from store.pagination import CollectionPagination
from store.serializers import ProductSerializer, CollectionSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer, HelpImageSerializer, CollectionProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CollectionViewSet(viewsets.ModelViewSet):
    pagination_class = CollectionPagination
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    @action(detail=True, methods=['get'], url_path='products')
    def get_products_of_collection(self, request, pk):
        products = Product.objects.filter(collection=pk)
        serializer = CollectionProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='latest-products')
    def get_latest_products_of_collection(self, request, pk):
        latest_products = Product.objects.filter(collection=pk, latest=True)
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


