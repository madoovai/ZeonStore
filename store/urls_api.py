from rest_framework.routers import DefaultRouter

from store.views import ProductViewSet, CollectionViewSet, AboutUsViewSet, NewsViewSet, \
    PublicOfferViewSet, HelpViewSet, FavoriteProductViewSet, ShoppingCartViewSet, OrderViewSet, SliderViewSet, \
    HitSaleProductsViewSet, LatestProductsViewSet, OurAdvantagesViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products_api')
router.register(r'favorite-products', FavoriteProductViewSet, basename='favorite_products_api')
router.register(r'bag', ShoppingCartViewSet, basename='bag_api')
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

urlpatterns = router.urls