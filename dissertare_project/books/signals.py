import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from books.models import Books
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


@receiver(pre_save, sender=Books)
def delete_old_book_image_file_signal(sender, instance:Books, **kwargs):
    """
    Exclui o arquivo de imagem do livro ao adicionar uma nova imagem
    """
    # Verifica se o livro já existe na base de dados
    if (Books.objects.filter(id=instance.id)):
        book = Books.objects.get(id=instance.id)
        new_book_image = instance.cover
        old_book_image = book.cover

        # verifica se o arquivo ou diretório existe
        if os.path.exists(old_book_image.path):
            # elimina a antiga imagem caso o usuário tenha carregado uma nova imagem
            if new_book_image != old_book_image:
                os.unlink(old_book_image.path)


@receiver(pre_save, sender=Books)
def delete_old_book_pdf_file_signal(sender, instance:Books, **kwargs):
    """
    Exclui o arquivo PDF do livro ao adicionar um novo PDF
    """
    # Verifica se o livro já existe na base de dados
    if (Books.objects.filter(id=instance.id)):
        book = Books.objects.get(id=instance.id)
        new_book_pdf = instance.file
        old_book_pdf = book.file

        # verifica se o arquivo ou diretório existe
        if os.path.exists(old_book_pdf.path):
            # elimina o antigo arquivo PDF caso o usuário tenha carregado um novo
            if new_book_pdf != old_book_pdf:
                os.unlink(old_book_pdf.path)
