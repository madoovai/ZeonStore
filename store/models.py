from colorfield.fields import ColorField
from django.db import models
from ckeditor.fields import RichTextField


class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Коллекция")
    image = models.ImageField(blank=True, null=True, verbose_name="Картинка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    articul = models.CharField(max_length=255, verbose_name="Артикул")
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

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', verbose_name="Товар", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Картинка")

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class ProductColor(models.Model):
    image = models.ForeignKey(ProductImage, related_name='colors', verbose_name="Картинка", on_delete=models.CASCADE, null=True)
    color = ColorField(verbose_name="Цвет", default='#FF0000')

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


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
    icon = models.ImageField(verbose_name="Иконка")
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


class Slyder(models.Model):
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

