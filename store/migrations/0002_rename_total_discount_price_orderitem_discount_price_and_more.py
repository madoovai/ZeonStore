# Generated by Django 4.0.4 on 2022-06-13 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='total_discount_price',
            new_name='discount_price',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='total_old_price',
            new_name='old_price',
        ),
    ]
