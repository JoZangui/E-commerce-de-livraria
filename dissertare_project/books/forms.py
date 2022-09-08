from django import forms
from django.forms import ModelForm

from .models import Books, Authors


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['file', 'title', 'cover', 'description']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Títule do livro',
                'maxlength': '50',
                'autofocus': True}),

            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            
            'description': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'adicione uma descrição para o livro',
                'maxlength': '400'})}


class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ['name', 'image', 'biography']
