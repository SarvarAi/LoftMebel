from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User

from .models import Category, Product
from .forms import ContactUserForm, RegistrationForm, LoginForm, EditAccountForm, \
    EditPasswordForm


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
        print(products)
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
    return render(request, 'store/product.html', context=context)


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
