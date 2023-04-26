from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import ContactUser, ShippingAddress, City


class ContactUserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input'
    }))

    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'contact__section-message',
        'cols': '30',
        'rows': '10'
    }))

    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'contact__section-input',
    }))

    class Meta:
        model = ContactUser
        fields = ('name', 'email', 'text', 'file')


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'username',
                  'password1',
                  'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))


class EditAccountForm(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Название аккаунта'
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваша фамилия'
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваша почта'
    }))

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email')


class EditPasswordForm(UserChangeForm):
    old_password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))

    new_password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))

    confirm_new_password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))

    class Meta:
        model = User
        fields = ('old_password',
                  'new_password',
                  'confirm_new_password')


class ShippingAddressForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label='Выберите город', widget=forms.Select(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваш город'
    }))

    class Meta:
        model = ShippingAddress
        fields = (
            'city',
            'address',
            'phone',
            'apartment_number')
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Ваш адрес'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Ваш номер телефона'
            }),
            'apartment_number': forms.NumberInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Номер аппартамента'
            })
        }
