import os, shutil

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from books.models import Books, Authors
from django.conf import settings

# media path
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


@receiver(pre_save, sender=Authors)
def delete_old_author_image_file_signal(sender, instance:Authors, **kwargs):
    """
    Exclui o arquivo de imagem do autor ao adicionar uma nova imagem
    """
    author = Authors.objects.get(id=instance.id)
    new_author_image = instance.image
    old_author_image = author.image

    # verifica se o arquivo ou diretório existe
    if os.path.exists(os.path.join(MEDIA_BASE_DIR, old_author_image.name)):
        # elimina a antiga imagem caso o usuário tenha carregado uma nova imagem
        if new_author_image != old_author_image:
            # caminho do directório media (configurado em settings.py)
            os.unlink(os.path.join(MEDIA_BASE_DIR, old_author_image.name)) # media/authors/images/author_name


@receiver(post_delete, sender=Authors)
def delete_author_files_signal(sender, instance:Authors,**kwargs):
    """
    Exclui o arquivo associado ao autor e limpa todos os atributos no campo quando excluir um autor da base de dados.
    """
    instance.image.delete(save=False)
