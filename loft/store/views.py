from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import reverse_lazy
import stripe

from .models import Category, Product, FavoriteProducts, HistoryProducts
from .forms import ContactUserForm, RegistrationForm, LoginForm, EditAccountForm, \
    EditPasswordForm, ShippingAddressForm, ShippingAddressPermanentForm, ShippingAddressPermanent
from .utils import CartForAuthenticatedUser
from loft import settings


# Create your views here.


class HomeView(ListView):
    template_name = 'store/home.html'
    model = Category
    context_object_name = 'products'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_queryset(self, *, object_list=None, **kwargs):
        products = Product.objects.all()
        return products


class SearchHomeView(HomeView):

    def get_queryset(self, **kwargs):
        _search_word = self.request.GET.get('search')
        products = Product.objects.filter(title__icontains=_search_word)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_word'] = self.request.GET.get('search')
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'store/category.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        products = Product.objects.filter(category__slug=slug)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        title = category.title
        context['title'] = f'{title}'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'

    def is_favorite_product(self, topic_product):
        if self.request.user.is_authenticated:
            user = self.request.user
            favorite_products = [i.product for i in user.favorite_products.all()]
            if topic_product in favorite_products:
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.all()
        topic_color = topic_product.colors.get(slug=self.kwargs['color_slug'])

        context['topic_product'] = topic_product
        context['products'] = products
        context['topic_color'] = topic_color
        context['title'] = f'Продукт: {topic_product.title}'

        if self.is_favorite_product(topic_product=topic_product):
            context['is_favorite'] = True

        return context


class AboutView(TemplateView):
    template_name = 'store/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'О нас'
        return context


def add_favorite_product(request, product_slug):
    if request.user.is_authenticated:
        user = request.user
        _product = Product.objects.get(slug=product_slug)
        if _product in [i.product for i in user.favorite_products.all()]:
            fav_product = FavoriteProducts.objects.get(user=user, product=_product)
            fav_product.delete()
            messages.error(request, 'Продукт удален из избранного')

        else:
            FavoriteProducts.objects.create(user=user, product=_product)
            messages.success(request, 'Продукт успешно добавлен в избранное')

        next_page = request.META.get('HTTP_REFERER', 'home')
        return redirect(next_page)
    else:
        messages.warning(request, 'Войдите или зарегистрируйтесь что бы добавить в Избранное')
        return redirect('registration')


def registration(request):
    form = RegistrationForm()
    context = {
        'title': 'Регистрация',
        'registration_form': form
    }
    return render(request, 'store/registration.html', context=context)


def registrate_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Войдите в Аккаунт')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
    return redirect('registration')


class ContactUsView(FormView):
    template_name = 'store/contact_us.html'
    form_class = ContactUserForm
    extra_context = {'title': 'Контакты'}

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Мы получили ваше сообщения, мы ответим вам в течении 1 дня')
        return redirect('home')


def login_page(request):
    form = LoginForm()
    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }
    return render(request, 'store/login.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно вашли в аккаунт')
                return redirect('home')
            else:
                messages.error(request, 'Не верное имя пользователя или пароль')
                return redirect('home')
        else:
            messages.error(request, 'Не верное имя пользователя или пароль')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Вход в аккаунт'
    }
    return render(request, 'store/login.html', context=context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы  вышли из аккаунта')
    return redirect('home')


def profile_page(request):
    form = EditAccountForm(instance=request.user if request.user.is_authenticated else None)
    context = {
        'title': 'Профиль',
        'form': form
    }
    history = HistoryProducts.objects.filter(user=request.user)

    if history:
        context['history'] = history

    return render(request, 'store/profile.html', context=context)


def change_password_page(request):
    form = EditPasswordForm()
    context = {
        'title': 'Измените пароль',
        'form': form
    }
    return render(request, 'store/change_password.html', context=context)


def changing_password(request):
    if request.method == 'POST':
        form = EditPasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            if user.check_password(data['old_password']):
                if data['old_password'] and data['new_password'] == data['confirm_new_password']:
                    user.set_password(data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.warning(request, 'Пароль успшно изменён')
                    return redirect('profile')
                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
            form.save()
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
        return redirect('profile')


def favorites(request):
    if request.user.is_authenticated:
        user = request.user
        favorite_products = [i.product for i in user.favorite_products.all()]
        context = {
            'title': 'Избранное',
            'products': favorite_products
        }
        return render(request, 'store/favorites.html', context=context)
    else:
        return redirect('registration')


def get_cart_information(request):
    if request.user.is_authenticated:
        cart = CartForAuthenticatedUser(request=request)
        context = cart.get_cart_info()
        favorite_products = [i.product for i in request.user.favorite_products.all()]
        context['title'] = 'Ваша корзина'
        context['products'] = favorite_products

        return render(request, 'store/basket.html', context=context)
    else:
        return redirect('registration')


def edit_profile_account(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
    return redirect('profile')


def cart_operation(request, order_product_slug, order_product_color, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, order_product_slug, order_product_color, action)
        next_page = request.META.get('HTTP_REFERER', 'home')
        return redirect(next_page)
    else:
        messages.error(request, 'Авторизуйтесь или зарегистрируйтесь')
        return redirect('registration')


def delete_order_product(request, order_product_slug, order_product_color):
    user_cart = CartForAuthenticatedUser(request, order_product_slug, order_product_color)
    next_page = request.META.get('HTTP_REFERER', 'home')
    return redirect(next_page)


def checkout(request):
    if request.method == 'POST':
        address = None
        try:
            address = ShippingAddressPermanent.objects.get(user=request.user)
        except:
            pass
        if address:
            form = ShippingAddressForm(instance=address)
            cart = CartForAuthenticatedUser(request=request)
            context = cart.get_cart_info()
            context['form'] = form
            context['title'] = 'Оформление заказа'
            return render(request, 'store/checkout.html', context=context)
        else:
            form = ShippingAddressForm
            cart = CartForAuthenticatedUser(request=request)
            context = cart.get_cart_info()
            context['form'] = form
            context['title'] = 'Оформление заказа'
            return render(request, 'store/checkout.html', context=context)
    else:
        return redirect('home')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request=request).get_cart_info()
        shipping_form = ShippingAddressForm(request.POST)

        if shipping_form.is_valid:
            address = shipping_form.save(commit=False)
            address.user = request.user
            address.order = user_cart['order']
            address.save()

            total_price = user_cart['cart_total_price']
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Товары с LoftMebel'
                        },
                        'unit_amount': int(total_price * 100)
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )
            return redirect(session.url, 303)

        else:
            for field in shipping_form.errors:
                messages.error(request, shipping_form.errors[field].as_text())
            return redirect('get_cart_information')


def success_payment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    messages.success(request, 'Оплата прошла успешно')
    return render(request, 'store/success.html')


class ShippingView(TemplateView):
    template_name = 'store/shipping.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = None
        try:
            address = ShippingAddressPermanent.objects.get(user=self.request.user)
        except:
            pass
        if address:
            context['form'] = ShippingAddressPermanentForm(instance=address)
        else:
            context['form'] = ShippingAddressPermanentForm()
        context['title'] = 'Адрес доставки'
        return context


def saving_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressPermanentForm(data=request.POST)
        if form.is_valid():
            last_address = None
            try:
                last_address = ShippingAddressPermanent.objects.get(user=request.user)
            except:
                pass
            if last_address:
                last_address.delete()
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, 'Адрес доставки успешно изменен')
                return redirect('home')
            else:
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                messages.success(request, 'Адрес доставки успешно сохранен')
                return redirect('home')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('shipping-address')
    else:
        return redirect('home')
