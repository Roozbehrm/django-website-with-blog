from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from captcha.fields import CaptchaField


class RegisterForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
    username = forms.CharField(label='Email / Username')