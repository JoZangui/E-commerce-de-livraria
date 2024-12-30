from django import forms
from django.forms import ModelForm

from .models import Books, Authors, Announcement


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['file', 'title', 'cover', 'description', 'comment', 'author', 'category', 'price', 'is_sale', 'sale_price']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Títule do livro',
                'maxlength': '50',
                'autofocus': True
            }),

            'cover': forms.FileInput(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'Sinopse do livro',
                'maxlength': '400',
                'style': "resize: none;"
            }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'Faça um comentário sobre este livro (História sobre o livro e ou seu autor, curiosidades, pontos marcantes...)',
                'maxlength': '400',
                'style': "resize: none;"
            }),
            'author': forms.Select(attrs={'class': "form-select"}),
            'category': forms.SelectMultiple(attrs={'class': "form-select", 'aria-label': "Multiple select example"}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input is_sale'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control sale_price'})
        }


class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ['name', 'image', 'biography']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Nome do autor',
                'maxlength': '50',
                'autofocus': True}),
            
            'image': forms.FileInput(attrs={'class': 'form-control'}),

            'biography': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'adicione uma biografia para o autor',
                'maxlength': '400'})
        }


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Título',
                'maxlength': '50',
                'autofocus': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control not-resizable',
                'cols':'30',
                'rows': '10',
                'placeholder': 'Descrição',
                'maxlength': '400'
            }),
            'image': forms.FileInput(
                attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'formFile'
                }
            )
        }
