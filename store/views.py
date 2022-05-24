from django.views.generic import TemplateView
from store.models import Product


from rest_framework.response import Response
from rest_framework.views import APIView


class ProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response({"products": products})


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class CollectionView(TemplateView):
    template_name = "collection.html"


class NewsView(TemplateView):
    template_name = "news.html"





