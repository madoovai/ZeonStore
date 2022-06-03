from rest_framework.routers import DefaultRouter

from store.views import ProductViewSet, CollectionViewSet, AboutUsViewSet, NewsViewSet, \
    PublicOfferViewSet, HelpViewSet, FavoriteProductViewSet, BagProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')
router.register(r'favorite-products', FavoriteProductViewSet, basename='favorite_products_api')
router.register(r'bag', BagProductViewSet, basename='bag_api')
router.register(r'order', OrderViewSet, basename='order_api')
router.register(r'collections', CollectionViewSet, basename='collections_api')
router.register(r'about-us', AboutUsViewSet, basename='about_us_api')
router.register(r'news', NewsViewSet, basename='news_api')
router.register(r'public-offer', PublicOfferViewSet, basename='public_offer_api')
router.register(r'help', HelpViewSet, basename='help_api')
# router.register(r'main-page', MainPageApiViewSet, basename='main_api')

urlpatterns = router.urls