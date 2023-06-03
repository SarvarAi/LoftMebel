from unittest import TestCase

from django.urls import reverse, resolve

from ..views import HomeView, AboutView, ContactUsView, SearchHomeView, CategoryView, \
    registration, registrate_user, ProductDetailView, user_login, login_page, profile_page, \
    user_logout, change_password_page, changing_password, add_favorite_product, favorites, \
    get_cart_information, edit_profile_account, cart_operation, delete_order_product, \
    checkout, create_checkout_session, success_payment, ShippingView, saving_shipping_address
from ..models import Category, Product


class TestUrls(TestCase):

    def setUp(self):
        self.products = Product.objects.all()

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func.view_class, AboutView)

    def test_contact_us_url_is_resolved(self):
        url = reverse('contact_us')
        self.assertEquals(resolve(url).func.view_class, ContactUsView)

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func.view_class, SearchHomeView)

    def test_category_url_is_resolved(self):
        categories = Category.objects.all()

        for category in categories:
            title = category.title
            url = reverse('category', args=[str(title)])
            self.assertEquals(resolve(url).func.view_class, CategoryView)

    def test_registration_url_is_resolved(self):
        url = reverse('registration')
        self.assertEquals(resolve(url).func, registration)

    def test_registrate_user_url_is_resolved(self):
        url = reverse('registrate_user')
        self.assertEquals(resolve(url).func, registrate_user)

    def test_product_url_is_resolved(self):
        for product in self.products:
            slug = product.slug
            color = product.get_first_color()

            url = reverse('product', kwargs={'slug': slug, 'color_slug': color})
            self.assertEquals(resolve(url).func.view_class, ProductDetailView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, user_login)

    def test_login_page_url_is_resolved(self):
        url = reverse('login_page')
        self.assertEquals(resolve(url).func, login_page)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile_page)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_change_password_url_is_resolved(self):
        url = reverse('change_password')
        self.assertEquals(resolve(url).func, change_password_page)

    def test_changing_password_url_is_resolved(self):
        url = reverse('changing_password')
        self.assertEquals(resolve(url).func, changing_password)

    def test_add_favorite_product_url_is_resolved(self):
        for product in self.products:
            url = reverse('add_favorite_product', args=[product.slug])
            self.assertEquals(resolve(url).func, add_favorite_product)

    def test_favorites_url_is_resolved(self):
        url = reverse('favorites')
        self.assertEquals(resolve(url).func, favorites)

    def test_get_cart_information_url_is_resolved(self):
        url = reverse('get_cart_information')
        self.assertEquals(resolve(url).func, get_cart_information)

    def test_edit_profile_account_url_is_resolved(self):
        url = reverse('edit_profile_account')
        self.assertEquals(resolve(url).func, edit_profile_account)

    def test_cart_operation_url_is_resolved(self):
        operations = ['add', 'delete']
        for product in self.products:
            for operation in operations:
                url = reverse('cart_operation', args=[product.slug, product.get_first_color(), operation])
                self.assertEquals(resolve(url).func, cart_operation)

    def test_delete_order_product_url_is_resolved(self):
        for product in self.products:
            url = reverse('delete_order_product', args=[product.slug, product.get_first_color()])
            self.assertEquals(resolve(url).func, delete_order_product)

    def test_checkout_url_is_resolved(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_create_checkout_session_url_is_resolved(self):
        url = reverse('create_checkout_session')
        self.assertEquals(resolve(url).func, create_checkout_session)

    def test_success_url_is_resolved(self):
        url = reverse('success')
        self.assertEquals(resolve(url).func, success_payment)

    def test_shipping_address_url_is_resolves(self):
        url = reverse('shipping-address')
        self.assertEquals(resolve(url).func.view_class, ShippingView)

    def test_saving_shipping_address_url_is_resolved(self):
        url = reverse('saving_shipping_address')
        self.assertEquals(resolve(url).func, saving_shipping_address)
