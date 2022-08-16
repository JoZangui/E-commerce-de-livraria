from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def books_pdf_file_path(instance, filename):
    """
    configura o diretório dos arquivos livros (PDF)
    para um directório com o nome do usuário
    """
    return f'books/pdfs/{instance.book_owner.username}/{filename}'


def books_image_file_path(instance, filename):
    """
    configura o diretório das capas dos livros (img)
    para um directório com o nome do usuário
    """
    return f'books/images/{instance.book_owner.username}/{filename}'


class Books(models.Model):
    book_file = models.FileField(upload_to=books_pdf_file_path, verbose_name='livro')
    book_title = models.CharField(max_length=50, verbose_name='Título do livro')
    book_description = models.TextField(max_length=400, verbose_name='Descrição do livro')
    book_cover = models.ImageField(
        upload_to=books_image_file_path,
        verbose_name='Capa do livro')
    date_posted = models.DateTimeField(default=timezone.now)
    book_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Proprietário do livro')

    def __str__(self) -> str:
        return self.book_title
