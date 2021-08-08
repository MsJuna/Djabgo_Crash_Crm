from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    
    if created:
        
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        username = instance.username
        email = instance.email
        
        Customer.objects.create(user=instance, name=username, email=email)
