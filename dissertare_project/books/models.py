import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .pdf_file_validator import pdf_format_validator


def val_cannot_be_negative(val):
    """ Verifica se o valor inserido pelo usuário é menor a zero """
    if val < 0:
        raise ValidationError(
            _("%(value)s é menor que zero, o valor não pode ser menor que zero"),
            params={'value': val}
        )


def books_pdf_file_path(instance, filename):
    """
    configura o diretório dos arquivos livros (PDF)
    """
    books_pdf_path = os.path.join('books', 'pdfs')
    return os.path.join(books_pdf_path, filename)


def books_image_file_path(instance, filename):
    """
    configura o diretório das capas dos livros (img)
    """
    books_image_path = os.path.join('books', 'images')
    return os.path.join(books_image_path, filename)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class Books(models.Model):

    author = models.CharField(max_length=50, verbose_name='Autor', default='unknow')
    file = models.FileField(
        upload_to=books_pdf_file_path,
        verbose_name='Arquivo',
        validators=[pdf_format_validator]
    )
    title = models.CharField(max_length=50, verbose_name='Título do livro')
    description = models.TextField(max_length=400, verbose_name='Sinopse')
    comment = models.TextField(max_length=400, verbose_name='Comentário', null=True, blank=True)
    cover = models.ImageField(
        upload_to=books_image_file_path,
        verbose_name='Capa do livro')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Publicado no site em')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Enviado por')
    category = models.ManyToManyField(Category, related_name='books_category', default=[0])
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6, validators=[val_cannot_be_negative])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6, validators=[val_cannot_be_negative], null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.cover.path)

        if img.height > 2500 or img.width > 1600:
            output_size = (2500, 1600)
            img.thumbnail(output_size)
            img.save(self.cover.path)

    class Meta:
        verbose_name_plural = 'Books'

class BookLists(models.Model):
    list_name = models.CharField(verbose_name='Nome da lista', max_length=50)
    books = models.ManyToManyField(Books, verbose_name='Livros', related_name='book_lists', default=[0])
    list_description = models.TextField(verbose_name='Descrição da lista')
    update_date = models.DateTimeField(default=timezone.now, verbose_name='Data da ultima actualização')

    def __str__(self) -> str:
        return self.list_name

    class Meta:
        verbose_name_plural = 'Book lists'

class Announcement(models.Model):
    title = models.CharField(verbose_name='Titulo do anúncio', max_length=50)
    description = models.TextField(verbose_name='Descrição', max_length=100)
    image = models.ImageField(upload_to='announcement', verbose_name='Imagem')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Data do upload')

    def __str__(self) -> str:
        return self.title
