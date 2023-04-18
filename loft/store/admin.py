from django.contrib import admin
from .models import Category, Product, Gallery, ContactUser
from django.utils.safestring import mark_safe


# Register your models here.

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
    inlines = [GalleryInline]

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
