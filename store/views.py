from rest_framework import viewsets, generics
from store.models import Product, Collection, About, News, PublicOffer, Help
from store.serializers import ProductSerializer, CollectionSerializer, SimilarProductSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class SimilarProductViewSet(viewsets.ModelViewSet):
    serializer_class = SimilarProductSerializer
    queryset = Product.objects.filter()


class CollectionViewSet(viewsets.ModelViewSet):

    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()


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


