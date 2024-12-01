""" payment models """
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save

from books.models import Books


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(default=timezone.now)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'Order - {str(self.id)}'


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {self.id}'


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_phone_number = models.CharField(max_length=20, blank=True)
    shipping_mode = models.CharField(verbose_name='Local de entrega', default='Home', max_length=50) # diz onde o cliente vai receber o produto, em casa ou na loja

    class Meta:
        verbose_name_plural = "Shipping Address"
    
    def __str__(self) -> str:
        return f'Shipping Address - {str(self.id)}'
    

class Invoices(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=10, verbose_name='Fatura nº', )
    invoice_file = models.FileField(upload_to='invoices', null=True, blank=True)

    def __str__(self) -> str:
        return f'Invoice nº {self.invoice_number}'

    class Meta:
        verbose_name_plural = 'Invoices'
