# Generated by Django 4.0.4 on 2022-05-27 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_slyder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slyder',
            name='link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Ссылка'),
        ),
    ]
