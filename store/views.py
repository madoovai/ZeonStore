from rest_framework import viewsets
from store.models import Product, Collection, About, News, PublicOffer, Help, ImageHelp
from store.serializers import ProductSerializer, CollectionSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer, HelpImageSerializer


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        help_image = ImageHelp.objects.all().first()
        if help_image:
            image_serializer = HelpImageSerializer(instance=help_image)
            response.data["image"] = image_serializer.data
        return response


