# Generated by Django 4.2 on 2023-04-26 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_historyproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyproducts',
            name='order_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Номер заказа'),
        ),
        migrations.AlterField(
            model_name='historyproducts',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукт'),
        ),
    ]
