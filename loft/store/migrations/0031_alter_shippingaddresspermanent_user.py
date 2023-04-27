# Generated by Django 4.2 on 2023-04-26 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0030_shippingaddresspermanent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddresspermanent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]