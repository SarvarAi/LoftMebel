import profile

from django.contrib.auth import logout
from django.urls import path

from .views import HomeView, AboutView, ContactUsView, SearchHomeView, CategoryView, \
    registration, registrate_user, ProductDetailView, user_login, login_page, profile_page, \
    user_logout, change_password_page, changing_password, add_favorite_product, favorites, \
    get_cart_information, edit_profile_account, cart_operation, delete_order_product, \
    checkout, create_checkout_session, success_payment, ShippingView, saving_shipping_address

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('search/', SearchHomeView.as_view(), name='search'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('register/', registration, name='registration'),
    path('registrate_user/', registrate_user, name='registrate_user'),
    path('product/<slug:slug>/<str:color_slug>/', ProductDetailView.as_view(), name='product'),
    path('login/', user_login, name='login'),
    path('login-page/', login_page, name='login_page'),
    path('profile/', profile_page, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password_page, name='change_password'),
    path('changing-password/', changing_password, name='changing_password'),
    path('add_favorite_product/<slug:product_slug>', add_favorite_product, name='add_favorite_product'),
    path('favorites/', favorites, name='favorites'),
    path('cart/', get_cart_information, name='get_cart_information'),
    path('edit_profile_account/', edit_profile_account, name='edit_profile_account'),
    path('cart_operation/<slug:order_product_slug>/<str:order_product_color>/<str:action>/', cart_operation,
         name='cart_operation'),
    path('delete_order_product/<slug:order_product_slug>/<str:order_product_color>/', delete_order_product,
         name='delete_order_product'),
    path('checkout/', checkout, name='checkout'),
    path('create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('success/', success_payment, name='success'),
    path('shipping-address/', ShippingView.as_view(), name='shipping-address'),
    path('saving-shipping-address/', saving_shipping_address, name='saving_shipping_address'),
]
