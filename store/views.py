from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404

from store.models import Product

from rest_framework.response import Response
from rest_framework.views import APIView

from store.serializers import ProductSerializer


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data})

    def post(self, request):
        product = request.data.get('product')

        serializer = ProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
        return Response({"success": "Product '{}' created successfully".format(product_saved.title)})

    def put(self, request, pk):
        saved_product = get_object_or_404(Product.objects.all(), pk=pk)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_product, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()

        return Response({"success": "Product '{}' updated successfully".format(product_saved.title)})

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        return Response({
            "message": "Product with id '{}' has been deleted".format(pk)
        })


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class NewsView(TemplateView):
    template_name = "news.html"





