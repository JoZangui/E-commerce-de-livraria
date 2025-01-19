""" payment signals """
from pathlib import Path
import json

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File

from .models import Order, ShippingAddress, Invoices
from .create_invoices import CreateInvoce


# Create a User ShippingAddress instance by default when user signs up
@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# Auto Add shippind Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = timezone.now()
        obj = sender._default_manager.get(pk=instance.pk)
        # Explicação no vídeo: 38, minuto: 7:05 https://www.youtube.com/watch?v=DHxgq2tH_TA&list=PLCC34OHNcOtpRfBYk-8y0GMO4i1p1zn50&index=39
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

# Create Invoices file when Invoice model is created
@receiver(post_save, sender=Invoices)
def create_invoice_file(sender, instance:Invoices, created, **kwargs):
    """ Cria um ficheiro de fatura e "armazena" na tabela Invoice """
    if created:
        shipping_address = json.loads(instance.order.shipping_address)
        
        cliente_info = {
            'full_name': instance.order.full_name,
            'email': instance.order.email,
            'shipping_address': f"Endereço 1: {shipping_address['shipping_address1']} / Endereço 2: {shipping_address['shipping_address2']}",
            'city': shipping_address['shipping_city'],
            'payment_mode': instance.payment_mode
        }

        create_invoce = CreateInvoce(
            cliente_email=cliente_info['email'],
            cliente_address=cliente_info['shipping_address'],
            cliente_city=cliente_info['city'],
            invoice_number=instance.invoice_number,
            payment_mode = cliente_info['payment_mode'],
            creation_date = timezone.now()
        )

        order_items = instance.order.orderitem_set.all()

        for order_item in order_items:
            quantity = order_item.quantity
            price = order_item.price
            title = order_item.book.title

            # adiciona os itens na tabela da fatura com o respectivo preço, quantidade e título do livro
            create_invoce.add_item(quantity, price, title)

        # salvando o arquivo na base de dados
        # https://docs.djangoproject.com/en/5.1/topics/files/#using-files-in-models
        invoice_file_path = Path(create_invoce.create_invoice_file())

        with invoice_file_path.open(mode='rb') as f:
            instance.invoice_file = File(f, name=invoice_file_path.name)
            instance.save()

        import os
        """
        Elimina o ficheiro que foi criado pelo método 'create_invoce.create_invoice_file()'
        deixando apenas o que foi carregado pelo Django FileFiled, evitando assim duplicidade de faturas
        """
        os.remove(create_invoce.create_invoice_file())

# Elimina os arquivos de faturas eliminadas na base de dados
@receiver(post_delete, sender=Invoices)
def delete_invoice_files(sender, instance:Invoices, **kwargs):
    """
    Exclui o arquivo associado ao invoice e limpa todos os atributos no campo quando excluir um Invoice. Nota: Este método fechará o arquivo se ele estiver aberto quando delete() for chamado.

    O argumento opcional save controla se a instância do modelo é salva ou não após a exclusão do arquivo associado a este campo. Padrões para True.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.fields.files.FieldFile.delete
    """
    instance.invoice_file.delete(save=False)
