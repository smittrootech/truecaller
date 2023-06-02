from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class SpamCounter(models.Model):
    contact_num=PhoneNumberField()
    spam= models.IntegerField(default=0)


class Contacts(models.Model):
    mobile_number= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='contact')
    first_name = models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    contact_numbers =PhoneNumberField()
    active=models.BooleanField(default=True)
    is_spam=models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    class Meta:
        unique_together=[["mobile_number","contact_numbers"]]

@receiver(post_save, sender=SpamCounter)
def update_contacts_spam_flag(sender, instance, **kwargs):
    if instance.spam == 25:
        try:
            Contacts.objects.filter(contact_numbers=instance.contact_num).update(is_spam=True)
            settings.AUTH_USER_MODEL.objects.filter(mobile_number=instance.contact_num).update(is_spam=True)
        except:
            pass
            