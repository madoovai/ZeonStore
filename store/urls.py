"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from store.urls_api import router
from store.views import HomeView, SearchProduct
from django.urls import include
from django.urls import path
from auth.views import RegisterView

schema_view = get_swagger_view(title='API for Store')

from store.views import ProductViewSet, CollectionViewSet, AboutUsViewSet, NewsViewSet, \
    PublicOfferViewSet, HelpViewSet, FavoriteProductViewSet, ShoppingCartViewSet, OrderViewSet, SliderViewSet, \
    HitSaleProductsViewSet, LatestProductsViewSet, OurAdvantagesViewSet, FooterViewSet, CallBackViewSet


# router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')
router.register(r'favorite-products', FavoriteProductViewSet, basename='favorite_products_api')
router.register(r'shopping-cart', ShoppingCartViewSet, basename='shopping_cart_api')
router.register(r'order', OrderViewSet, basename='order_api')
router.register(r'collections', CollectionViewSet, basename='collections_api')
router.register(r'about-us', AboutUsViewSet, basename='about_us_api')
router.register(r'news', NewsViewSet, basename='news_api')
router.register(r'public-offer', PublicOfferViewSet, basename='public_offer_api')
router.register(r'help', HelpViewSet, basename='help_api')
router.register(r'slider', SliderViewSet, basename='slider_api')
router.register(r'hitsale-product', HitSaleProductsViewSet, basename='hitsale_product_api')
router.register(r'latest-product', LatestProductsViewSet, basename='latest_product_api')
router.register(r'our-advantages', OurAdvantagesViewSet, basename='our_advantages_api')
router.register(r'footer', FooterViewSet, basename='footer_api')
router.register(r'call-back', CallBackViewSet, basename='callback_api')


urlpatterns = [
    path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('swagger/', schema_view),
    path('search/', SearchProduct.as_view(), name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls