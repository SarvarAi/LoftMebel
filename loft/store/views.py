from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User

from .models import Category, Product, FavoriteProducts
from .forms import ContactUserForm, RegistrationForm, LoginForm, EditAccountForm, \
    EditPasswordForm
from .utils import CartForAuthenticatedUser


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


def product(request, slug):
    topic_product = Product.objects.get(slug=slug)
    products = Product.objects.all()
    context = {
        'topic_product': topic_product,
        'products': products,
        'title': f'Продукт: {topic_product.title}'
    }

    if request.user.is_authenticated:
        user = request.user
        favorite_products = [i.product for i in user.favorite_products.all()]

        if topic_product in favorite_products:
            is_favorite = True
        else:
            is_favorite = False

        context['is_favorite'] = is_favorite

    return render(request, 'store/product.html', context=context)


def product_color(request, product_slug, color_slug):
    topic_product = Product.objects.get(slug=product_slug)
    topic_color = topic_product.colors.get(slug=color_slug)
    products = Product.objects.all()
    context = {
        'topic_product': topic_product,
        'products': products,
        'topic_color': topic_color,
        'title': f'Продукт: {topic_product.title}'
    }
    return render(request, 'store/product.html', context=context)


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


class AboutView(TemplateView):
    template_name = 'store/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'О нас'
        return context


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


def contact_us(request):
    context = {
        'title': 'Контакты',
        'contact_user_form': ContactUserForm(),
    }
    return render(request, 'store/contact_us.html', context=context)


def saving_user_contacts(request):
    if request.method == 'POST':
        form = ContactUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

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
        redirect('registration')


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
        redirect('registration')
