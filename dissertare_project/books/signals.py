import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from books.models import Books, Authors
from django.conf import settings


# caminho do directório 'media' (configurado em settings.py)
MEDIA_BASE_DIR = settings.MEDIA_ROOT

@receiver(post_delete, sender=Books)
def delete_book_files_signal(sender, instance:Books,**kwargs):
    """
    Exclui o arquivo associado ao livro e limpa todos os atributos no campo quando excluir um livro. Nota: Este método fechará o arquivo se ele estiver aberto quando delete() for chamado.

    O argumento opcional save controla se a instância do modelo é salva ou não após a exclusão do arquivo associado a este campo. Padrões para True.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.fields.files.FieldFile.delete
    """
    instance.file.delete(save=False)
    instance.cover.delete(save=False)


@receiver(pre_save, sender=Books)
def update_book_files_signal(sender, instance:Books, **kwargs):
    """
    Exclui o arquivo de imagem e de pdf do livro ao actualizar os dados do mesmo
    caso o usuário tenha carregado uma outra imagem ou ficheiro pdf
    """

    try:
        book = Books.objects.get(pk=instance.pk)
        new_book_cover = instance.cover
        new_book_file = instance.file
        old_book_cover = book.cover
        old_book_file = book.file

        # elimina a antiga imagem caso o usuário tenha carregado uma nova imagem
        if new_book_cover != old_book_cover:
            os.unlink(os.path.join(MEDIA_BASE_DIR, old_book_cover.name))

        # elimina o antigo ficheiro pdf caso o usuário tenha carregado um novo
        if new_book_file != old_book_file:
            os.unlink(os.path.join(MEDIA_BASE_DIR, old_book_file.name))
    except Exception:
        return None


@receiver(pre_save, sender=Authors)
def update_author_image_file_signal(sender, instance:Authors, **kwargs):
    """
    Exclui o arquivo de imagem do autor ao actualizar os dados do mesmo
    caso o usuário tenha carregado uma outra imagem
    """

    try:
        author = Authors.objects.get(pk=instance.pk)
        new_author_image = instance.image
        old_author_image = author.image

        # elimina a antiga imagem caso o usuário tenha carregado uma nova imagem
        if new_author_image != old_author_image:
            os.unlink(os.path.join(MEDIA_BASE_DIR, old_author_image.name))
    except Exception:
        return None


@receiver(post_delete, sender=Authors)
def delete_author_image_file_signal(sender, instance:Authors,**kwargs):
    """
    Exclui o arquivo associado ao autor e limpa todos os atributos no campo quando excluir um autor.
    """

    instance.image.delete(save=False)
