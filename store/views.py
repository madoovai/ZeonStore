from rest_framework import viewsets
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CollectionViewSet(viewsets.ModelViewSet):

    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()



