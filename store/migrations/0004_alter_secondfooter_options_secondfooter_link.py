# Generated by Django 4.0.4 on 2022-06-13 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_secondfooter_options_remove_secondfooter_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='secondfooter',
            options={'verbose_name': 'Вторая вкладка', 'verbose_name_plural': 'Вторая вкладка'},
        ),
        migrations.AddField(
            model_name='secondfooter',
            name='link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.footer'),
        ),
    ]
