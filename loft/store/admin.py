from django.contrib import admin
from .models import Category, Product, Gallery, ContactUser, AvailableColors, \
    FavoriteProducts, Order, OrderProduct, City, ShippingAddress, HistoryProducts, ShippingAddressPermanent
from django.utils.safestring import mark_safe


# Register your models here.
class AvailableColorsInline(admin.TabularInline):
    fk_name = 'product'
    model = AvailableColors
    extra = 1
    prepopulated_fields = {'slug': ('color_name',), }


class GalleryInline(admin.TabularInline):
    fk_name = 'Product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'svg', 'svg_mobile')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',), }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'quantity_in_storage', 'color', 'price', 'rating')
    list_display_links = ('title', 'category')
    list_editable = ('quantity_in_storage',)
    prepopulated_fields = {'slug': ('title',), }
    inlines = [GalleryInline, AvailableColorsInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = "Product's photo"


@admin.register(ContactUser)
class ContactUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')
    list_display_links = ('name',)


@admin.register(FavoriteProducts)
class FavoriteProductsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_display_links = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_at', 'is_completed', 'shipping')
    list_display_links = ('user',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'added_at')
    list_display_links = ('order',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)
    list_display_links = ('city',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'city', 'phone')
    list_display_links = ('user', 'order')


@admin.register(HistoryProducts)
class HistoryProductsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'order_number', 'price')
    list_display_links = ('user',)


@admin.register(ShippingAddressPermanent)
class ShippingAddressPermanentAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'address', 'phone', 'apartment_number')
    list_display_links = ('user',)
