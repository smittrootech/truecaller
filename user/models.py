from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from contacts.models import Contacts
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# #################################################
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, mobile_number, password, **extra_fields):
        """Create and save a User with the given email and password."""
        # if not email:
        #     raise ValueError('The given email must be set')
        # email = self.normalize_email(mobile_number)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('roles', User.Role.Admin.name)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    class Role(models.TextChoices):
        User = 'U' ,_('User')
        Admin = 'A', _('Admin')

    username=None
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    roles = models.CharField(max_length=50, choices = Role.choices)
    mobile_number=PhoneNumberField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password=models.CharField(max_length=100)
    is_spam=models.BooleanField(default=False)


    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.mobile_number)


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, created, **kwargs):
#     if created:
#         Contacts.objects.get_or_create(
#             mobile_number=instance.mobile_number,
#             first_name=instance.first_name,
#             last_name=instance.last_name,
#             contact_numbers=instance.mobile_number,
#             is_spam=instance.is_spam
#         )