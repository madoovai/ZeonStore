from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class CollectionView(TemplateView):
    template_name = "collection.html"


class NewsView(TemplateView):
    template_name = "news.html"





