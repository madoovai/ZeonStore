from rest_framework.routers import DefaultRouter

from store.views import ProductViewSet, CollectionViewSet, SimilarProductViewSet, AboutUsViewSet, NewsViewSet, \
    PublicOfferViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')
router.register(r'similar-products', SimilarProductViewSet, basename='similar_products_api')
router.register(r'collections', CollectionViewSet, basename='collections_api')
router.register(r'about-us', AboutUsViewSet, basename='about_us_api')
router.register(r'news', NewsViewSet, basename='news_api')
router.register(r'public-offer', PublicOfferViewSet, basename='public_offer_api')

urlpatterns = router.urls