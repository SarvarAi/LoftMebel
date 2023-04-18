from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Category')
    svg = models.FileField(null=True, blank=True, upload_to='category/', verbose_name='Image svg')
    svg_mobile = models.FileField(null=True, blank=True, upload_to='category/mobile_svg',
                                  verbose_name='Image mobile svg')
    slug = models.SlugField(verbose_name='Slug', unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

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
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

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


class Gallery(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='images')
    image = models.ImageField(upload_to='gallery/', verbose_name='Image')

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
        verbose_name = 'User Contact'
        verbose_name_plural = 'User Contacts'

# class Client(models.Model):
#     name = models.CharField(max_length=255, verbose_name='Name')
#     surname = models.CharField(maxlength=255, verbose_name='Surname')
#     email = models.EmailField(max_length=255, verbose_name='Email')
#     telephone_number = models.CharField(max_length=255, verbose_name='Phone number')
#     password = models.CharField(max_length=255, verbose_name='Password')
#


