from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from contacts.models import Contacts

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Contacts.objects.get_or_create(
            mobile_number=instance.mobile_number,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
