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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.IntegerField(verbose_name="Количество линеек")
    color_id = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.CASCADE)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True)
    discount_price = models.IntegerField(verbose_name="Цена со скидкой", null=True)
    title = models.CharField(verbose_name="Название", max_length=50, null=True)
    size_line = models.CharField(verbose_name="Размер", max_length=20, null=True)

    def __str__(self):
        return self.product_id.title

    def save(self, *args, **kwargs):
        product = Product.objects.get(id=self.product_id.id)
        self.old_price = product.old_price
        self.discount_price = product.discount_price
        self.title = product.title
        self.size_line = product.size_line
        super(Bag, self).save(*args, **kwargs)
        #метод для стягивания полей(цены, название, резмер) с продукта, который пришел в запросе
        #и сохранение в модели Корзина

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"



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






