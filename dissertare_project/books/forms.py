from django import forms
from django.forms import ModelForm

from .models import Books


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['book_file', 'book_title', 'book_cover', 'book_description']

        widgets = {
            'book_file': forms.FileInput(attrs={'class': 'form-control'}),

            'book_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Títule do livro',
                'maxlength': '50',
                'autofocus': True}),

            'book_cover': forms.FileInput(attrs={'class': 'form-control'}),
            
            'book_description': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'adicione uma descrição para o livro',
                'maxlength': '400'})}
