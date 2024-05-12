from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm
)
from django import forms

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'lnr lnr-user form-control',
            'placeholder': 'Имя',
            'icon_class': 'lnr lnr-user'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'lnr lnr-user form-control',
            'placeholder': 'Фамилия',
            'icon_class': 'lnr lnr-user'
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'lnr lnr-envelope form-control',
            'placeholder': 'Электронная почта',
            'icon_class': 'lnr lnr-envelope'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'lnr lnr-lock form-control',
            'placeholder': 'Пароль',
            'icon_class': 'lnr lnr-lock'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'lnr lnr-lock form-control',
            'placeholder': 'Подтверждение пароля',
            'icon_class': 'lnr lnr-lock'
        }
    ))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'lnr lnr-envelope form-control',
            'placeholder': 'Email',
            'type': 'email',
            'icon_class': 'lnr lnr-envelope'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'lnr lnr-lock form-control',
            'placeholder': 'Пароль',
            'type': "password",
            'icon_class': 'lnr lnr-lock'
        }
    ))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'lnr lnr-envelope form-control',
            'placeholder': 'Электронная почта',
            'icon_class': 'lnr lnr-envelope'
        }
    ))
