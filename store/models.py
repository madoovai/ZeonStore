from colorfield.fields import ColorField
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from store.validators import validate_file_extension


class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Коллекция")
    image = models.ImageField(blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class Color(models.Model):
    name = models.CharField(verbose_name="Название цвета", max_length=30)
    rgb = ColorField(verbose_name="Цвет RGB")

    def __str__(self):
        return f"{self.name} ({self.rgb})"

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class ProductLine(models.Model):
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
    hit = models.BooleanField(verbose_name="Хит продаж", blank=True, null=True)
    latest = models.BooleanField(verbose_name="Новинки", blank=True, null=True)
    favorite = models.BooleanField(verbose_name="Избранное", blank=True, null=True)

    def __str__(self):
        return self.title

    def similar_products(self):
        similar_products = ProductLine.objects.filter(collection=self.collection).exclude(id=self.id)
        return similar_products

    def save(self, *args, **kwargs):
        self.discount = 100 - (self.discount_price * 100 / self.old_price)
        super(ProductLine, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(ProductLine, related_name='images', verbose_name="Товар", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Картинка")
    color = models.ForeignKey(Color, related_name="images", verbose_name="Цвет", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class OrderItem(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)
    image = models.ForeignKey(ProductImage, verbose_name="Фото", on_delete=models.CASCADE, null=True)
    amount_of_productline = models.IntegerField(verbose_name="Количество линеек")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объект заказа"
        verbose_name_plural = "Объекты заказа"


class Order(models.Model):
    amount_of_productlines = models.IntegerField(verbose_name="Количество линеек")
    total_number_of_products = models.IntegerField(verbose_name="Количество товаров")
    total_price_without_discount = models.IntegerField(verbose_name="Общая цена без скидки")
    total_price_with_discount = models.IntegerField(verbose_name="Общая цена со скидкой")
    final_total_price = models.IntegerField(verbose_name="Итого цена")

    def __int__(self):
        return self.id

    def save(self, *args, **kwargs):
        """
        Метод для оформления заказа, стягивание и суммирование данных с Корзины
        """
        self.amount_of_productlines = ShoppingCart.objects.filter(order=self.id).aggregate(Sum('amount_of_productline')).get('amount_of_productline__sum')
        self.total_number_of_products = ShoppingCart.total_number_of_products_in_shoppingcart()
        self.total_price_without_discount = ShoppingCart.all_products_total_old_price()
        self.total_price_with_discount = ShoppingCart.all_products_total_discount_price()
        self.final_total_price = self.total_price_with_discount - self.total_price_without_discount
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ShoppingCart(models.Model):
    product = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    amount_of_productline = models.IntegerField(verbose_name="Количество линеек")
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    total_old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    total_discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    title = models.CharField(verbose_name="Название", max_length=50, null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)
    image = models.ForeignKey(ProductImage, verbose_name="Фото", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
    total_amount_of_productline = models.IntegerField(verbose_name="Общее количество товаров", null=True)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        """
        1. метод для стягивания полей(цены, название, резмер, фото) с продукта,
        который пришел в запросе и сохранение объекта в модели Корзина
        2. Создание этого же объекта в модели OrderItem
        """
        product = self.product
        image = ProductImage.objects.get(product=self.product, color=self.color)
        self.total_old_price = product.old_price * self.amount_of_productline
        self.total_discount_price = product.discount_price * self.amount_of_productline
        self.title = product.title
        self.size_line = product.size_line
        self.image = image
        self.total_amount_of_productline = product.product_amount * self.amount_of_productline
        OrderItem.objects.create(title=self.title, color=self.color, image=self.image, old_price=self.total_old_price,
                                 discount_price=self.total_discount_price, size_line=self.size_line,
                                 amount_of_productline=self.amount_of_productline)
        super(ShoppingCart, self).save(*args, **kwargs)

    @staticmethod
    def total_number_of_products_in_shoppingcart():
        """
        Расчет общего колво товаров исходя из колво линеек в Корзине
        :return: total_number_of_products
        """
        total_number_of_products = 0
        for product in ShoppingCart.objects.all():
            total_number_of_products += product.total_amount_of_productline
            return total_number_of_products

    @staticmethod
    def all_products_total_old_price():
        """
        Расчет общей старой цены всех товаров исходя из колво линеек в Корзине
        :return: total_old_price
        """
        total_old_price = 0
        for product in ShoppingCart.objects.all():
            total_old_price += product.total_old_price
            return total_old_price

    @staticmethod
    def all_products_total_discount_price():
        """
        Расчет общей старой цены всех товаров исходя из колво линеек в Корзине
        :return: total_old_price
        """
        total_discount_price = 0
        for product in ShoppingCart.objects.all():
            total_discount_price += product.total_discount_price
            return total_discount_price

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class User(models.Model):
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
    order_date = models.DateField(verbose_name="Дата оформления")
    order_status = models.CharField(verbose_name="Статус заказа", max_length=50, choices=ORDER_STATUSES, default="new")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class About(models.Model):
    headline = models.CharField(verbose_name="Заголовок", max_length=50)
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class AboutImage(models.Model):
    page = models.ForeignKey(About, related_name="images", verbose_name="Страница", null=True, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фотография", null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии о нас"


class OurAdvantage(models.Model):
    icon = models.FileField(verbose_name="Иконка", validators=[validate_file_extension])
    #валидатор по формату загружаемоего файла, допустимо только .svg or .png
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = models.CharField(max_length=200, verbose_name="Описание")

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Наше преимущество"
        verbose_name_plural = "Наши преимущества"


class News(models.Model):
    photo = models.ImageField(verbose_name="Фотография")
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Slider(models.Model):
    photo = models.ImageField(verbose_name="Фотография")
    link = models.CharField(verbose_name="Ссылка", max_length=250, null=True, blank=True)

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = "Слайдер"


class PublicOffer(models.Model):
    headline = models.CharField(max_length=20, verbose_name="Заголовок")
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Публичная офферта"
        verbose_name_plural = "Публичные офферты"


class ImageHelp(models.Model):
    image = models.ImageField(verbose_name="Фотография")

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Изображение для Помощь"
        verbose_name_plural = "Изображение для Помощь"


class Help(models.Model):
    question = models.CharField(max_length=200, verbose_name="Вопрос")
    answer = models.CharField(max_length=500, verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Помощь"
        verbose_name_plural = "Помощь"


class Footer(models.Model):
    logotype = models.ImageField(verbose_name="Логотип")
    text_info = models.CharField(verbose_name="Текстовая информация", max_length=500)
    phone_number = models.IntegerField(verbose_name="Номер")

    def __str__(self):
        return self.text_info

    class Meta:
        verbose_name = "Футер"
        verbose_name_plural = "Футер"


class SecondFooter(models.Model):
    TYPE = (
        ("number", _("Телефон")),
        ("email", _("Почта")),
        ("Instagram", _("Инстаграм")),
        ("Telegram", _("Телеграм")),
        ("WhatsApp", _("WhatsApp"))
    )
    link = models.ForeignKey(Footer, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Тип", choices=TYPE, max_length=50)
    input_field = models.CharField(verbose_name="Поле для заполнения", max_length=500)

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        if self.type is 'WhatsApp':
            self.input_field = 'https://wa.me/' + self.input_field
        super(SecondFooter, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Вторая вкладка"
        verbose_name_plural = "Вторая вкладка"
