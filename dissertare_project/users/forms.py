""" users forms """
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',  'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'nome de utilizador'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro Nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ultimo nome'})
        }
