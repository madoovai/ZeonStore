from django.shortcuts import redirect
from django.views import View
from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import ProductLine, Collection, About, News, PublicOffer, Help, \
    ImageHelp, ShoppingCart, Slider, OurAdvantage, Order, OrderItem, Footer, CallBack, SecondFooter
from store.pagination import TwelvePagination, EightPagination
from store.serializers import ProductSerializer, CollectionSerializer, AboutUsSerializer, \
    NewsSerializer, PublicOfferSerializer, HelpSerializer, HelpImageSerializer, CollectionProductSerializer, \
    FavoriteProductSerializer, SliderSerializer, HitSaleProductsSerializer, \
    LatestProductsSerializer, OurAdvantagesSerializer, OrderSerializer, ShoppingCartSerializer, FooterSerializer, \
    CallBackSerializer, SearchProductSerializer, SecondFooterSerializer


class HomeView(View):
    def dispatch(self, request, *args, **kwargs):
        return redirect("/admin")


class ProductViewSet(viewsets.ModelViewSet):
    """viewset для Товаров"""
    serializer_class = ProductSerializer
    queryset = ProductLine.objects.all()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """viewset для Корзины"""
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()

    def get_total_number_of_productlines_in_shoppingcart(self):
        """
        Суммирование количества линеек исходя из колво товарных линеек в Корзине
        :return: total_number_of_productlines
        """
        total_number_of_productlines = 0
        for product in ShoppingCart.objects.all():
            total_number_of_productlines += product.amount_of_productline
        return total_number_of_productlines

    def get_total_number_of_products_in_shoppingcart(self):
        """
        Суммирование колво товаров исходя из колво линеек в Корзине
        :return: total_number_of_products
        """
        total_number_of_products = 0
        for order_item in ShoppingCart.objects.all():
            total_number_of_products += order_item.amount_of_productline * order_item.product.product_amount
        return total_number_of_products

    def get_total_old_price(self):
        """
        Суммирование старой цены всех товаров исходя из колво линеек в Корзине
        :return: total_old_price
        """
        total_old_price = 0
        for product in ShoppingCart.objects.all():
            total_old_price += product.old_price * product.amount_of_productline
        return total_old_price

    def get_total_discount(self):
        """
        Суммирование скидки всех товаров исходя из колво линеек в Корзине
        :return: total_discount_price
        """
        total_discount = 0
        for product in ShoppingCart.objects.all():
            total_discount += (product.old_price - product.discount_price) * product.amount_of_productline
        return total_discount

    def list(self, request, *args, **kwargs):
        """Метод для отображения сумм, количества линеек и товаров в Корзине"""
        response = super().list(request, *args, **kwargs)
        response.data["total_number_of_productlines"] = self.get_total_number_of_productlines_in_shoppingcart()
        response.data["total_number_of_products"] = self.get_total_number_of_products_in_shoppingcart()
        response.data["total_old_price"] = self.get_total_old_price()
        response.data["total_discount"] = self.get_total_discount()
        response.data["total_final_price"] = self.get_total_old_price() - self.get_total_discount()
        return response


class OrderViewSet(viewsets.ModelViewSet):
    """
    Создание заказа
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        """Метод для сохранения объекта Заказ с последующим клонированием объектов с Корзины в модель
        Объект Заказа и опустошением Корзины для новых заказов
        + вызов метода для подсчета инфо о заказе"""
        order = serializer.save()

        for item in ShoppingCart.objects.all():
            OrderItem.objects.create(title=item.title, color=item.color, image=item.image,
                                     old_price=item.old_price, order=order,
                                     discount_price=item.discount_price, size_line=item.size_line,
                                     amount_of_productline=item.amount_of_productline, product=item.product)
        order.calculate_order_data()

        ShoppingCart.objects.all().delete()


def random_products():
    """
    метод для 5 рандомных уникальных товаров c филтрацией по коллекции
    """
    random_products = []
    random_collections = []

    collections_count = 5
    if Collection.objects.count() < 5:
        collections_count = Collection.objects.count()

    for i in range(collections_count):
        random_collection = Collection.objects.order_by('?').first()
        while random_collection in random_collections:
            random_collection = Collection.objects.order_by('?').first()

        random_collections.append(random_collection)
        filtered_products = ProductLine.objects.filter(collection=random_collection)
        random_product = filtered_products.order_by('?').first()
        if random_product:
            random_products.append(random_product)

    return random_products


class FavoriteProductViewSet(viewsets.ModelViewSet):
    """
    отображение Избранных товаров в API с проверкой если товаров в Избранном нет,
    то вызывается метод для рандомных товаров (метод находится выше)
    + пагинация 12
    """
    queryset = ProductLine.objects.filter(favorite=True)
    serializer_class = FavoriteProductSerializer
    pagination_class = TwelvePagination

    def get_queryset(self):
        queryset = ProductLine.objects.filter(favorite=True)
        if len(queryset) == 0:
            return random_products()
        else:
            return queryset

    def list(self, request, *args, **kwargs):
        """Метод для передачи в response количества избранных товаров"""
        response = super().list(request, *args, **kwargs)
        amount_of_favorite_products = len(ProductLine.objects.filter(favorite=True))
        response.data["amount_of_favorite_products"] = amount_of_favorite_products
        return response


class CollectionViewSet(viewsets.ModelViewSet):
    """viewset для Коллекции"""
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    pagination_class = EightPagination

    @action(detail=True, methods=['get'], url_path='products')
    def get_products_of_collection(self, request, pk):
        """
        декоратор для отображения отфильтрованных по коллекции продуктов в API + пагинация
        """
        products = ProductLine.objects.filter(collection=pk)
        paginator = TwelvePagination()
        page = paginator.paginate_queryset(products, request)
        serializer = CollectionProductSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'], url_path='latest-products')
    def get_latest_products_of_collection(self, request, pk):
        """
        декоратор для отображения отфильтрованных по коллекции продуктов со статусом "Новинка" в API + пагинация
        """
        latest_products = ProductLine.objects.filter(collection=pk, latest=True)
        serializer = CollectionProductSerializer(latest_products, many=True)
        return Response(serializer.data)


class AboutUsViewSet(viewsets.ModelViewSet):
    """viewset для О нас"""
    serializer_class = AboutUsSerializer
    queryset = About.objects.all()


class NewsViewSet(viewsets.ModelViewSet):
    """viewset для Новости"""
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class PublicOfferViewSet(viewsets.ModelViewSet):
    """viewset для Публичная офферта"""
    serializer_class = PublicOfferSerializer
    queryset = PublicOffer.objects.all()


class HelpViewSet(viewsets.ModelViewSet):
    """viewset для Помощи"""
    serializer_class = HelpSerializer
    queryset = Help.objects.all()

    def list(self, request, *args, **kwargs):
        """Метод для передачи только 1 изображения для раздела Помощь"""
        response = super().list(request, *args, **kwargs)
        help_image = ImageHelp.objects.all().first()
        if help_image:
            image_serializer = HelpImageSerializer(instance=help_image)
            response.data["image"] = image_serializer.data
        return response


class SliderViewSet(viewsets.ModelViewSet):
    """viewset для Слайдер"""
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HitSaleProductsViewSet(viewsets.ModelViewSet):
    """viewset для продуктов со статусом Хиты Продаж"""
    serializer_class = HitSaleProductsSerializer
    queryset = ProductLine.objects.filter(hit=True)
    pagination_class = EightPagination


class LatestProductsViewSet(viewsets.ModelViewSet):
    """viewset для продуктов со статусом Новинка"""
    serializer_class = LatestProductsSerializer
    queryset = ProductLine.objects.filter(latest=True)
    pagination_class = EightPagination


class OurAdvantagesViewSet(viewsets.ModelViewSet):
    """viewset для Наши преимущества"""
    serializer_class = OurAdvantagesSerializer
    queryset = OurAdvantage.objects.all()


class FooterViewSet(viewsets.ModelViewSet):
    """viewset для Футер"""
    serializer_class = FooterSerializer
    queryset = Footer.objects.all()


class CallBackViewSet(viewsets.ModelViewSet):
    """viewset для Обратный звонок"""
    serializer_class = CallBackSerializer
    queryset = CallBack.objects.all()


class SearchProduct(generics.ListAPIView):
    """Поиск товара по названию + пагинация 8"""
    queryset = ProductLine.objects.all()
    serializer_class = SearchProductSerializer
    search_fields = ['title',]
    pagination_class = EightPagination

    def get_queryset(self):
        """метод для проверки наличия результата поиска,
        если нет то вызов функции рандомных товаров"""
        keyword = self.request.query_params.get('search', '')
        queryset = ProductLine.objects.filter(title__icontains=keyword)

        if len(queryset) == 0:
            return random_products()
        else:
            return queryset

    def list(self, request, *args, **kwargs):
        """Метод для передачи в response Ключевого слова с поисковика"""
        response = super().list(request, *args, **kwargs)
        search_word = self.request.GET.get('search')
        response.data["search_keyword"] = search_word
        return response