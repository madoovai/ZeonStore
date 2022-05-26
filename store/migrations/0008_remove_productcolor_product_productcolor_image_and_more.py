# Generated by Django 4.0.4 on 2022-05-26 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_status_product_hit_product_latest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcolor',
            name='product',
        ),
        migrations.AddField(
            model_name='productcolor',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='store.productimage', verbose_name='Картинка'),
        ),
        migrations.DeleteModel(
            name='ProductSizeLine',
        ),
    ]
