# Generated by Django 4.2 on 2023-04-26 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_historyproducts_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyproducts',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
    ]
