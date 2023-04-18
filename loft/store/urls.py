import profile

from django.contrib.auth import logout
from django.urls import path

from .views import HomeView, SearchHomeView, CategoryView, AboutView, contact_us, \
    registrate_user, saving_user_contacts, registration, product, user_login, login_page, \
    profile_page, user_logout, changing_password, change_password_page

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact_us/', contact_us, name='contact_us'),
    path('save_contact/', saving_user_contacts, name='save_contact'),
    path('search/', SearchHomeView.as_view(), name='search'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('register/', registration, name='registration'),
    path('registrate_user/', registrate_user, name='registrate_user'),
    path('product/<slug:slug>', product, name='product'),
    path('login/', user_login, name='login'),
    path('login-page/', login_page, name='login_page'),
    path('profile/', profile_page, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password_page, name='change_password'),
    path('changing-password/', changing_password, name='changing_password'),
]
