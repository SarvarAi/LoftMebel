from django import template
from store.models import Category, FavoriteProducts

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_footer_categories():
    categories = Category.objects.all()
    footer_categories, footer_subcategories = [], []
    index = 0

    for category in categories:
        if len(footer_subcategories) >= 3:
            temp = footer_subcategories.copy()
            footer_categories.append(temp)
            footer_subcategories.clear()
            if len(categories[index::]) <= 3:
                footer_categories += [categories[index::]]

        index += 1
        footer_subcategories.append(category)

    return footer_categories


@register.simple_tag()
def get_favorite_products(user):
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
