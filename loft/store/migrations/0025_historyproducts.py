# Generated by Django 4.2 on 2023-04-26 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0024_remove_order_apartment_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(default=0, verbose_name='Номер заказа')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Купленый продукт',
                'verbose_name_plural': 'Купленые продукты',
            },
        ),
    ]
