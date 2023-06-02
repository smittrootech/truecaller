from django.contrib import admin
from .models import Contacts,SpamCounter

# Register your models here.

@admin.register(Contacts)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('mobile_number','first_name', 'last_name', 'contact_numbers','active','is_spam')
    search_fields = ('mobile_number','first_name', 'last_name', 'contact_numbers','active')
    ordering = ('first_name','contact_numbers')
    
@admin.register(SpamCounter)
class SpamAdmin(admin.ModelAdmin):
    list_display=('contact_num','spam')