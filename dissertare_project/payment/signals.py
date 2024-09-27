""" payment signals """
from pathlib import Path

from django.db.models.signals import post_save, pre_save
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
    if created:
        create_invoce = CreateInvoce('Client Name', 'cliente@email.com', '933333333', 'Urbanização Nova Vida')
        
        order_items = instance.order.orderitem_set.all()

        for order_item in order_items:
            quantity = order_item.quantity
            price = order_item.price
            title = order_item.book.title

            create_invoce.add_item(quantity, price, title)

        # salvando o arquivo na base de dados
        # https://docs.djangoproject.com/en/5.1/topics/files/#using-files-in-models
        invoice_file_path = Path(create_invoce.create_invoice_file())
        
        with invoice_file_path.open(mode='rb') as f:
            instance.invoice_file = File(f, name=invoice_file_path.name)
            instance.save()
