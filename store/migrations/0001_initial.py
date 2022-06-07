# Generated by Django 4.0.4 on 2022-06-06 16:20

import ckeditor.fields
import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import store.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'О нас',
                'verbose_name_plural': 'О нас',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Коллекция')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Коллекция',
                'verbose_name_plural': 'Коллекции',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название цвета')),
                ('rgb', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='Цвет RGB')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
            },
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logotype', models.ImageField(upload_to='', verbose_name='Логотип')),
                ('text_info', models.CharField(max_length=500, verbose_name='Текстовая информация')),
                ('phone_number', models.IntegerField(verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Футер',
                'verbose_name_plural': 'Футер',
            },
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('answer', models.CharField(max_length=500, verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Помощь',
                'verbose_name_plural': 'Помощь',
            },
        ),
        migrations.CreateModel(
            name='ImageHelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Изображение для Помощь',
                'verbose_name_plural': 'Изображение для Помощь',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Фотография')),
                ('headline', models.CharField(max_length=20, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('email', models.CharField(max_length=50, verbose_name='Электронная почта')),
                ('phone_number', models.IntegerField(verbose_name='Номер телефона')),
                ('country', models.CharField(max_length=50, verbose_name='Страна')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Дата оформления')),
                ('order_status', models.CharField(choices=[('new', 'Новый'), ('order_done', 'Оформлен'), ('cancelled', 'Отменен')], default='new', max_length=50, verbose_name='Статус заказа')),
                ('amount_of_productlines', models.IntegerField(default=0, verbose_name='Количество линеек')),
                ('total_number_of_products', models.IntegerField(default=0, verbose_name='Количество товаров')),
                ('total_price_without_discount', models.IntegerField(default=0, verbose_name='Общая цена без скидки')),
                ('total_price_with_discount', models.IntegerField(default=0, verbose_name='Общая цена со скидкой')),
                ('final_total_price', models.IntegerField(default=0, verbose_name='Итого цена')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OurAdvantage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.FileField(upload_to='', validators=[store.validators.validate_file_extension], verbose_name='Иконка')),
                ('headline', models.CharField(max_length=20, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Наше преимущество',
                'verbose_name_plural': 'Наши преимущества',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.color', verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('articul', models.CharField(max_length=255, verbose_name='Артикул')),
                ('discount_price', models.IntegerField(verbose_name='Цена со скидкой')),
                ('old_price', models.IntegerField(verbose_name='Цена без скидки')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание')),
                ('fabric_structure', models.CharField(max_length=100, null=True, verbose_name='Состав ткани')),
                ('fabric', models.CharField(max_length=100, null=True, verbose_name='Материал')),
                ('discount', models.IntegerField(verbose_name='Скидка')),
                ('size_line', models.CharField(max_length=10, null=True, verbose_name='Размерный ряд')),
                ('product_amount', models.IntegerField(blank=True, null=True, verbose_name='Количество в линейке')),
                ('hit', models.BooleanField(blank=True, null=True, verbose_name='Хит продаж')),
                ('latest', models.BooleanField(blank=True, null=True, verbose_name='Новинки')),
                ('favorite', models.BooleanField(blank=True, null=True, verbose_name='Избранное')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.collection', verbose_name='Коллекция')),
                ('colors', models.ManyToManyField(to='store.color', verbose_name='Цвета')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='PublicOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=20, verbose_name='Заголовок')),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Публичная офферта',
                'verbose_name_plural': 'Публичные офферты',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Фотография')),
                ('link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Слайдер',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_of_productline', models.IntegerField(verbose_name='Количество линеек')),
                ('total_old_price', models.IntegerField(null=True, verbose_name='Старая цена')),
                ('total_discount_price', models.IntegerField(null=True, verbose_name='Цена со скидкой')),
                ('title', models.CharField(max_length=50, null=True, verbose_name='Название')),
                ('size_line', models.CharField(max_length=20, null=True, verbose_name='Размер')),
                ('total_amount_of_productline', models.IntegerField(null=True, verbose_name='Общее количество товаров')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color', verbose_name='Цвет')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.productimage', verbose_name='Фото')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productline')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.CreateModel(
            name='SecondFooter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('number', 'Телефон'), ('email', 'Почта'), ('Instagram', 'Инстаграм'), ('Telegram', 'Телеграм'), ('WhatsApp', 'WhatsApp')], max_length=50, verbose_name='Тип')),
                ('input_field', models.CharField(max_length=500, verbose_name='Поле для заполнения')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.footer')),
            ],
            options={
                'verbose_name': 'Вторая вкладка',
                'verbose_name_plural': 'Вторая вкладка',
            },
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.productline', verbose_name='Товар'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('total_old_price', models.IntegerField(null=True, verbose_name='Старая цена')),
                ('total_discount_price', models.IntegerField(null=True, verbose_name='Цена со скидкой')),
                ('size_line', models.CharField(max_length=20, null=True, verbose_name='Размер')),
                ('amount_of_productline', models.IntegerField(verbose_name='Количество линеек')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color', verbose_name='Цвет')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.productimage', verbose_name='Фото')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productline', verbose_name='Линейка')),
            ],
            options={
                'verbose_name': 'Объект заказа',
                'verbose_name_plural': 'Объекты заказа',
            },
        ),
        migrations.CreateModel(
            name='AboutImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Фотография')),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.about', verbose_name='Страница')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии о нас',
            },
        ),
    ]
