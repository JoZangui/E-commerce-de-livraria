from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from users.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance:User, created, **kwargs):
    """ Cria um novo perfil quando um novo usuário for criado """
    
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()
