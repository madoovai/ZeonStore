# Generated by Django 4.0.4 on 2022-06-01 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_product_colors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_of_product', models.IntegerField(verbose_name='Количество линеек')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(to='store.color', verbose_name='Цвета'),
        ),
        migrations.DeleteModel(
            name='ProductColor',
        ),
        migrations.AddField(
            model_name='bag',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='bag',
            name='selected_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productimage'),
        ),
    ]