from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from store.validators import validate_file_extension


class Collection(models.Model):
    """Админка Коллекций"""
    title = models.CharField(max_length=200, verbose_name="Коллекция")
    image = models.ImageField(blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class Color(models.Model):
    """Админка Цветов"""
    name = models.CharField(verbose_name="Название цвета", max_length=30)
    rgb = ColorField(verbose_name="Цвет RGB")

    def __str__(self):
        return f"{self.name} ({self.rgb})"

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class ProductLine(models.Model):
    """Админка Товара"""
    title = models.CharField(max_length=255, verbose_name="Название товара")
    articul = models.CharField(max_length=255, verbose_name="Артикул")
    colors = models.ManyToManyField(Color, verbose_name="Цвета")
    discount_price = models.IntegerField(verbose_name="Цена со скидкой")
    old_price = models.IntegerField(verbose_name="Цена без скидки")
    description = RichTextField(verbose_name="Описание")
    fabric_structure = models.CharField(verbose_name="Состав ткани", max_length=100, null=True)
    fabric = models.CharField(verbose_name="Материал", max_length=100, null=True)
    discount = models.IntegerField(verbose_name="Скидка")
    size_line = models.CharField(verbose_name="Размерный ряд", max_length=10, null=True)
    product_amount = models.IntegerField(verbose_name="Количество в линейке", null=True, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="Коллекция", on_delete=models.CASCADE)
    hit = models.BooleanField(verbose_name="Хит продаж")
    latest = models.BooleanField(verbose_name="Новинки")
    favorite = models.BooleanField(verbose_name="Избранное")

    def __str__(self):
        return self.title

    def similar_products(self):
        """метод для филтрации товаров по коллекции для Похожих товаров"""
        similar_products = ProductLine.objects.filter(collection=self.collection).exclude(id=self.id)
        return similar_products

    def save(self, *args, **kwargs):
        """переопределение поля Скидка, авторасчет скидки исходя из старой и новой цены товара"""
        self.discount = 100 - (self.discount_price * 100 / self.old_price)
        super(ProductLine, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class UserFavoriteProduct(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    productline_id = models.ForeignKey(ProductLine, verbose_name="Избранный товар", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Избранный товар пользователя"
        verbose_name_plural = "Избранные товары пользователя"


class ProductImage(models.Model):
    """Админка Изображений Товара"""
    product = models.ForeignKey(ProductLine, related_name='images', verbose_name="Товар", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Картинка")
    color = models.ForeignKey(Color, related_name="images", verbose_name="Цвет", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Order(models.Model):
    """
    Модель Заказ с полями пользователя и расчета цен и колво товаров в заказе
    """
    ORDER_STATUSES = (
        ("new", _("Новый")),
        ("order_done", _("Оформлен")),
        ("cancelled", _("Отменен")),
    )

    name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    email = models.CharField(verbose_name="Электронная почта", max_length=50)
    phone_number = models.IntegerField(verbose_name="Номер телефона")
    country = models.CharField(verbose_name="Страна", max_length=50)
    city = models.CharField(verbose_name="Город", max_length=50)
    order_date = models.DateField(verbose_name="Дата оформления", auto_now_add=True)
    order_status = models.CharField(verbose_name="Статус заказа", max_length=50, choices=ORDER_STATUSES, default="new")

    amount_of_productlines = models.IntegerField(verbose_name="Количество линеек", default=0)
    total_number_of_products = models.IntegerField(verbose_name="Количество товаров", default=0)
    total_price_without_discount = models.IntegerField(verbose_name="Общая цена без скидки", default=0)
    total_discount = models.IntegerField(verbose_name="Общая скидка", default=0)
    final_total_price = models.IntegerField(verbose_name="Итого цена", default=0)

    def __str__(self):
        return f"Заказ {self.id}"

    def calculate_order_data(self):
        """
        Метод для оформления заказа, стягивание и суммирование данных с Корзины
        """
        self.amount_of_productlines = self.total_number_of_productlines_in_order()
        self.total_number_of_products = self.total_number_of_products_in_order()
        self.total_price_without_discount = self.total_old_price_in_order()
        self.total_discount = self.total_price_without_discount - self.total_discount_in_order()
        self.final_total_price = self.total_price_without_discount - self.total_discount

        self.save()

    def total_number_of_productlines_in_order(self):
        """
        Расчет общего колво линеек исходя из колво линеек в Корзине
        :return: total_number_of_productlines
        """
        total_number_of_productlines = 0
        for product in OrderItem.objects.filter(order=self):
            total_number_of_productlines += product.amount_of_productline
        return total_number_of_productlines

    def total_number_of_products_in_order(self):
        """
        Расчет общего колво товаров исходя из колво линеек в Корзине
        :return: total_number_of_products
        """
        total_number_of_products = 0
        for order_item in OrderItem.objects.filter(order=self):
            total_number_of_products += order_item.amount_of_productline * order_item.product.product_amount
        return total_number_of_products

    def total_old_price_in_order(self):
        """
        Расчет общей старой цены всех товаров исходя из колво линеек в Корзине
        :return: total_old_price
        """
        total_old_price = 0
        for product in OrderItem.objects.filter(order=self):
            total_old_price += product.old_price * product.amount_of_productline
        return total_old_price

    def total_discount_in_order(self):
        """
        Расчет общей скидки всех товаров исходя из колво линеек в Корзине
        :return: total_discount_price
        """
        total_discount_price = 0
        for product in OrderItem.objects.filter(order=self):
            total_discount_price += product.discount_price * product.amount_of_productline
        return total_discount_price

    def order_items(self):
        """
        Фильтрация товаров по Заказу
        """
        order_items = OrderItem.objects.filter(order=self)
        return order_items

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    """Админка Объекты Заказа"""
    product = models.ForeignKey(ProductLine, verbose_name="Линейка", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=200)
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)
    image = models.ForeignKey(ProductImage, verbose_name="Фото", on_delete=models.CASCADE, null=True)
    amount_of_productline = models.IntegerField(verbose_name="Количество линеек")
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объект заказа"
        verbose_name_plural = "Объекты заказа"


class ShoppingCart(models.Model):
    """Модель Корзины"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    amount_of_productline = models.IntegerField(verbose_name="Количество линеек")
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    title = models.CharField(verbose_name="Название", max_length=50, null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)
    image = models.ForeignKey(ProductImage, verbose_name="Фото", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        """
        метод для стягивания полей(цены, название, резмер, фото) с продукта,
        который пришел в запросе и сохранение объекта в модели Корзина
        """
        image = ProductImage.objects.get(product=self.product, color=self.color)
        self.image = image
        product = self.product
        self.old_price = product.old_price
        self.discount_price = product.discount_price
        self.title = product.title
        self.size_line = product.size_line
        super(ShoppingCart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class About(models.Model):
    """Админка О нас"""
    headline = models.CharField(verbose_name="Заголовок", max_length=50)
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class AboutImage(models.Model):
    """Админка Изображение для О нас"""
    page = models.ForeignKey(About, related_name="images", verbose_name="Страница", null=True, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фотография", null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии о нас"


class OurAdvantage(models.Model):
    """
    - Админка Наши преимущества
    - валидатор по формату загружаемоего файла, допустимо только .svg or .png
    """
    icon = models.FileField(verbose_name="Иконка", validators=[validate_file_extension])
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = models.CharField(max_length=200, verbose_name="Описание")

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Наше преимущество"
        verbose_name_plural = "Наши преимущества"


class News(models.Model):
    """Админка Новости"""
    photo = models.ImageField(verbose_name="Фотография")
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Slider(models.Model):
    """Админка Слайдер"""
    photo = models.ImageField(verbose_name="Фотография")
    link = models.CharField(verbose_name="Ссылка", max_length=250, null=True, blank=True)

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер"


class PublicOffer(models.Model):
    """Админка Публичная Офферта"""
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Публичная офферта"
        verbose_name_plural = "Публичная офферта"


class ImageHelp(models.Model):
    """Админка Изображеие для Помощь"""
    image = models.ImageField(verbose_name="Фотография")

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Изображение для Помощь"
        verbose_name_plural = "Изображение для Помощь"


class Help(models.Model):
    """Админка Помощь"""
    question = models.CharField(max_length=200, verbose_name="Вопрос")
    answer = models.CharField(max_length=500, verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Помощь"
        verbose_name_plural = "Помощь"


class Footer(models.Model):
    """
    Футер первая вкладка
    """
    logotype = models.ImageField(verbose_name="Логотип")
    text_info = models.CharField(verbose_name="Текстовая информация", max_length=500)
    phone_number = models.IntegerField(verbose_name="Номер")

    def __str__(self):
        return self.text_info

    def numbers_and_social_media(self):
        """Метод для получения объектов со Второй Вкладки по ссылке
        Это для API"""
        numbers_and_social_media = SecondFooter.objects.filter(link=self)
        return numbers_and_social_media

    class Meta:
        verbose_name = "Футер"
        verbose_name_plural = "Футер"


class SecondFooter(models.Model):
    """Футер вторая вкладка"""
    TYPE = (
        ("number", _("Телефон")),
        ("email", _("Почта")),
        ("instagram", _("Инстаграм")),
        ("telegram", _("Телеграм")),
        ("whatsapp", _("WhatsApp"))
    )
    link = models.ForeignKey(Footer, on_delete=models.CASCADE, null=True)
    type = models.CharField(verbose_name="Тип", choices=TYPE, max_length=50)
    input_field = models.CharField(verbose_name="Поле для заполнения", max_length=500)

    def save(self, *args, **kwargs):
        """Метод для проверки поля "whatsapp" и конвертация этого поля в ссылку"""
        if self.type == "whatsapp" and self.input_field.startswith('0') and len(self.input_field) == 10:
            self.input_field = self.input_field[1:]
            self.input_field = f"https://wa.me/996{self.input_field}"

        if self.type == "whatsapp" and len(self.input_field) == 9:
            self.input_field = f"https://wa.me/996{self.input_field}"

        if self.type == "whatsapp" and len(self.input_field) <= 9:
            return ValidationError("Need more that 9 numbers")

        super(SecondFooter, self).save(*args, **kwargs)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Вторая вкладка"
        verbose_name_plural = "Вторая вкладка"


class CallBack(models.Model):
    """Моделька Обратного звонка"""
    name = models.CharField(verbose_name="Имя", max_length=200)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=100)
    call_received_date = models.DateField(verbose_name="Дата обращения", auto_now_add=True)
    callback_type = models.CharField(verbose_name="Тип обращения", default="Обратный звонок", max_length=200)
    called_back = models.BooleanField(verbose_name="Статус позвонили?", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Обратный звонок"
        verbose_name_plural = "Обратный звонок"
