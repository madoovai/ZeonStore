from colorfield.fields import ColorField
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Sum

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


class Product(models.Model):
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
        similar_products = Product.objects.filter(collection=self.collection).exclude(id=self.id)
        return similar_products

    def hit_sale_products(self):
        hit_sale_products = Product.objects.filter(hit=True)
        return hit_sale_products

    def latest_products(self):
        latest_products = Product.objects.filter(latest=True)
        return latest_products

    def save(self, *args, **kwargs):
        self.discount = 100 - (self.discount_price * 100 / self.old_price)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', verbose_name="Товар", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Картинка")
    color = models.ForeignKey(Color, related_name="images", verbose_name="Цвет", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Bag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.IntegerField(verbose_name="Количество линеек")
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    title = models.CharField(verbose_name="Название", max_length=50, null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)
    image = models.ForeignKey(ProductImage, verbose_name="Фото", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        '''
        метод для стягивания полей(цены, название, резмер, фото) с продукта,
        который пришел в запросе и сохранение объекта в модели Корзина
        '''
        product = self.product
        image = ProductImage.objects.get(product=self.product, color=self.color)
        self.old_price = product.old_price
        self.discount_price = product.discount_price
        self.title = product.title
        self.size_line = product.size_line
        self.image = image
        super(Bag, self).save(*args, **kwargs)

    def total_number_of_products(self):
        '''
        Расчет общего колво товаров исходя из колво линеек в Корзине
        :return: total_number_of_products
        '''
        product = self.product
        self.amount_of_product = Bag.objects.get(product=product)
        total_number_of_products = product.product_amount * self.amount_of_product
        return total_number_of_products

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Order(models.Model):
    amount_of_products = models.IntegerField(verbose_name="Количество линеек")
    total_number_of_products = models.IntegerField(verbose_name="Количество товаров")
    total_price_without_discount = models.IntegerField(verbose_name="Общая цена без скидки")
    total_price_with_discount = models.IntegerField(verbose_name="Общая цена со скидкой")
    final_total_price = models.IntegerField(verbose_name="Итого цена")

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        '''
        Метод для оформления заказа, стягивание и суммирование данных с Корзины
        '''
        self.amount_of_products = Bag.objects.aggregate(Sum('amount_of_product')).get('amount_of_product__sum')
        self.total_number_of_products = Bag.objects.aggregate(Sum(Bag.total_number_of_products(self.total_number_of_products)))
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class About(models.Model):
    headline = models.CharField(verbose_name="Заголовок", max_length=50)
    description = RichTextField()

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "О нас"


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






