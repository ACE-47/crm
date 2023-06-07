from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'User Name',
        'class' : 'w-full my-4 py-4 px-4 bg-gray-100 rounded-xl text-xl',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        'class' : 'w-full my-4 py-4 px-4 bg-gray-100 rounded-xl text-xl',
    }))