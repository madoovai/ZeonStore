# Generated by Django 4.0.4 on 2022-05-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_publicoffer_description'),
    ]

    operations = [
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
    ]