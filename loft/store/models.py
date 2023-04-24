from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    svg = models.FileField(null=True, blank=True, upload_to='category/', verbose_name='Картина svg')
    svg_mobile = models.FileField(null=True, blank=True, upload_to='category/mobile_svg',
                                  verbose_name='Картнина мобильной версии svg')
    slug = models.SlugField(verbose_name='Слаг', unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    color = models.CharField(max_length=255, default='Black', verbose_name='Color')
    rating = models.FloatField(default=0, verbose_name='Rating')
    quantity_in_storage = models.IntegerField(default=0, verbose_name='Quantity')
    description = models.TextField(default='Here will be description of product', verbose_name='Discreption')
    depth = models.FloatField(default=0, verbose_name='Depth')
    width = models.FloatField(default=0, verbose_name='Width')
    height = models.FloatField(default=0, verbose_name='Height')
    slug = models.SlugField(verbose_name='Slug', unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_first_image(self):
        error_image = 'https://www.autoglushitel.com/wp-content/uploads/2018/12/13124-600x600.jpg'
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return error_image
        else:
            return error_image

    def get_first_color(self):
        return self.colors.first()


class Gallery(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='images')
    image = models.ImageField(upload_to='gallery/', verbose_name='Image')

    def __str__(self):
        return 'Галерея'

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'


class ContactUser(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    email = models.EmailField(max_length=255, verbose_name='Email')
    text = models.TextField(verbose_name='Text')
    file = models.FileField(upload_to='contacts_file/', null=True, blank=True, verbose_name='File')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт пользователя'
        verbose_name_plural = 'Котакты пользователей'


class AvailableColors(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=255, verbose_name='Цвет')
    color_code = models.CharField(max_length=255, verbose_name='Код цвета')
    slug = models.SlugField(verbose_name='Slug', null=True)

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class FavoriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products',
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный товар')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добаления заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Закончен ли заказ')
    shipping = models.BooleanField(default=False, verbose_name='Опция доставки')

    def __str__(self):
        return str(self.pk) + ' '

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    color_title = models.CharField(max_length=255, verbose_name='Цвет')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления продукта')

    def __str__(self):
        return self.product.title

    def get_color_code(self):
        colors = self.product.colors.all()
        for color in colors:
            if color.slug == self.color_title:
                return color.color_code
        return 'red'

    def get_color_name(self):
        colors = self.product.colors.all()
        for color in colors:
            if color.slug == self.color_title:
                return color.color_name
        return 'Ошибка'

    @property
    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Заказанный продукт'
        verbose_name_plural = 'Заказанные продукты'
