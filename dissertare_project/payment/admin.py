""" payment admin """
from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, Invoices

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Invoices)