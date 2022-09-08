from django.db.models.signals import post_delete
from django.dispatch import receiver

from books.models import Books


@receiver(post_delete, sender=Books)
def delete_post_signal(sender, instance:Books,**kwargs):
    """
    Exclui o arquivo associado a esta instância e limpa todos os atributos no campo. Nota: Este método fechará o arquivo se ele estiver aberto quando delete()for chamado.

    O argumento opcional save controla se a instância do modelo é salva ou não após a exclusão do arquivo associado a este campo. Padrões para True.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.fields.files.FieldFile.delete
    """
    instance.file.delete(save=False)
    instance.cover.delete(save=False)
