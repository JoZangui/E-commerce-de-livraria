import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from PIL import Image

from .pdf_file_validator import pdf_format_validator


def books_pdf_file_path(instance, filename):
    """
    configura o diretório dos arquivos livros (PDF)
    para um directório com o nome do usuário
    """
    books_pdf_path = os.path.join('books', 'pdfs')
    return os.path.join(books_pdf_path, str(instance.author.id), filename)


def books_image_file_path(instance, filename):
    """
    configura o diretório das capas dos livros (img)
    para um directório com o nome do usuário
    """
    books_image_path = os.path.join('books', 'images')
    return os.path.join(books_image_path, str(instance.author.id), filename)


def authors_image_file_path(instance, filename):
    """
    configura o diretório das imagens dos autores dos livros
    para um directório com o nome do usuário
    """
    authors_path = os.path.join('authors', 'images')
    return os.path.join(authors_path, str(instance.id), filename)


class Authors(models.Model):

    name = models.CharField(max_length=30, verbose_name='Nome do autor')
    image = models.ImageField(
        upload_to=authors_image_file_path,
        verbose_name='Imagem do autor',
        blank=True)
    biography = models.TextField(max_length=400, verbose_name='Biografia do autor')
    registration_date = models.DateTimeField(default=timezone.now, verbose_name='Registado em')

    def __str__(self) -> str:
        return f'ID: {self.id} - Nome: {self.name}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 940 or img.width > 640:
            output_size = (940, 640)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name_plural = 'Authors'

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class Books(models.Model):

    author = models.ForeignKey(Authors, on_delete=models.CASCADE, verbose_name='Autor do livro')
    file = models.FileField(
        upload_to=books_pdf_file_path,
        verbose_name='Arquivo',
        validators=[pdf_format_validator]
    )
    title = models.CharField(max_length=50, verbose_name='Título do livro')
    description = models.TextField(max_length=400, verbose_name='Descrição do livro')
    cover = models.ImageField(
        upload_to=books_image_file_path,
        verbose_name='Capa do livro')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Publicado no site em')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Enviado por')
    category = models.ManyToManyField(Category, default=1)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.cover.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.cover.path)

    class Meta:
        verbose_name_plural = 'Books'

class BookLists(models.Model):
    list_name = models.CharField(verbose_name='Nome da lista', max_length=50)
    books = models.ManyToManyField('Books', verbose_name='Livros', related_name='book_lists')
    list_description = models.TextField(verbose_name='Descrição da lista')

    def __str__(self) -> str:
        return self.list_name

    class Meta:
        verbose_name_plural = 'Book lists'
