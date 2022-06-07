# Generated by Django 4.0.4 on 2022-06-07 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondfooter',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.footer', verbose_name='Ссылка на футер'),
        ),
        migrations.AlterField(
            model_name='secondfooter',
            name='type',
            field=models.CharField(choices=[('number', 'Телефон'), ('email', 'Почта'), ('instagram', 'Инстаграм'), ('telegram', 'Телеграм'), ('whatsapp', 'WhatsApp')], max_length=50, verbose_name='Тип'),
        ),
    ]