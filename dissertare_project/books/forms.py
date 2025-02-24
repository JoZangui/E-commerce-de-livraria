from django import forms
from django.forms import ModelForm

from .models import Books, Announcement


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

            'category': forms.SelectMultiple(attrs={
                'class': "form-select",
                'aria-label': "Multiple select example"
            }),

            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),

            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input is_sale'}),

            'sale_price': forms.NumberInput(attrs={'class': 'form-control sale_price', 'min': 0})
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
