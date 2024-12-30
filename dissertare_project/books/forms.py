from django import forms
from django.forms import ModelForm

from .models import Books, Authors, Announcement


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['file', 'title', 'cover', 'description', 'author']

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
