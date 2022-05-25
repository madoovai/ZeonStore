from django.db import models
from ckeditor.fields import RichTextField


class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Коллекция")
    images = models.ImageField(upload_to='static/images', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class ProductStatusChoices(models.TextChoices):
    SALESHIT = "sales_hit", "Saleshit"
    LATEST = "latest", "Latest"


class Color(models.Model):
    color = models.CharField(max_length=20, verbose_name="Цвет")

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class SizeLine(models.Model):
    size = models.CharField(max_length=4, verbose_name="Размер", blank=True, null=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "Размерный ряд"
        verbose_name_plural = "Размерные ряды"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    articul = models.CharField(max_length=255, verbose_name="Артикул")
    colors = models.ManyToManyField(Color, related_name="colors")
    discount_price = models.IntegerField(verbose_name="Цена со скидкой")
    old_price = models.IntegerField(verbose_name="Цена без скидки")
    description = RichTextField()
    size_line = models.ManyToManyField(SizeLine, related_name="size_lines")
    fabric_structure = models.CharField(max_length=100, verbose_name="Состав ткани")
    discount = models.IntegerField(verbose_name="Скидка")
    collection = models.ForeignKey(Collection, verbose_name="Коллекция", on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус", choices=ProductStatusChoices.choices, max_length=20, default=None,
                              null=True, blank=True)
    favorite = models.BooleanField(verbose_name="Избранное", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', verbose_name="Товар", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Картинка")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"






