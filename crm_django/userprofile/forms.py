from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

INPUT_CLASS = 'w-full my-4 py-4 px-4 bg-gray-100 rounded-xl text-xl'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'User Name',
        'class' : INPUT_CLASS,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        'class' : INPUT_CLASS,
    }))


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'User Name',
        'class' : INPUT_CLASS,
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder' : 'Email',
        'class' : INPUT_CLASS,
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Your Password',
        'class' : INPUT_CLASS,
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Repeat Pawword',
        'class' : INPUT_CLASS,
    }))
    
    