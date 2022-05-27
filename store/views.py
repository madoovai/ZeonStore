from rest_framework import viewsets, generics
from store.models import Product, Collection, About
from store.serializers import ProductSerializer, CollectionSerializer, SimilarProductSerializer, AboutUsSerializer


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


