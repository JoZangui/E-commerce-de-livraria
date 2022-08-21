from dataclasses import fields
from django import forms
from django.forms import ModelForm

from .models import Books


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['book_file', 'book_title', 'book_cover', 'book_description']
