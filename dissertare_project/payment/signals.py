""" payment signals """
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Order, ShippingAddress

# Create a User ShippingAddress instance by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)

# Auto Add shippind Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = timezone.now()
        obj = sender._default_manager.get(pk=instance.pk)
        # Explicação no vídeo 38 minuto 7:05 https://www.youtube.com/watch?v=DHxgq2tH_TA&list=PLCC34OHNcOtpRfBYk-8y0GMO4i1p1zn50&index=39
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now