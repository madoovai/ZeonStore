from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Коллекция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class ProductStatusChoices(models.TextChoices):
    SALESHIT = "sales_hit", "Saleshit"
    LATEST = "latest", "Latest"


class ProductColorChoices(models.TextChoices):
    BLUE = "blue", "Blue"
    GREEN = "green", "Green"
    PINK = "pink", "Pink"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    articul = models.CharField(max_length=255, verbose_name="Артикул")
    color = models.CharField(verbose_name="Цвет", max_length=20,
                             choices=ProductColorChoices.choices, default=ProductColorChoices.BLUE, blank=True, null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой")
    old_price = models.IntegerField(verbose_name="Цена без скидки")
    description = models.CharField(max_length=500, verbose_name="Описание товара")
    size_line = models.IntegerField(verbose_name="Размерный ряд")
    fabric_structure = models.CharField(max_length=100, verbose_name="Состав ткани")
    amount_of_product = models.IntegerField(verbose_name="Количество")
    size = models.IntegerField(verbose_name="Размер")
    discount = models.IntegerField(verbose_name="Скидка")
    collection = models.ForeignKey(Collection, verbose_name="Коллекция", on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус", choices=ProductStatusChoices.choices, max_length=20, default=None,
                              null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"




