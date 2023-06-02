from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('mobile_number', 'password','roles')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name','last_name','password1', 'password2'),
        }),
    )
    list_display = ('mobile_number', 'first_name', 'last_name', 'created_at','is_spam','is_staff','roles')
    search_fields = ('mobile_number', 'first_name', 'last_name','created_at','roles')
    ordering = ('created_at',)
    # readonly_fields = ['created_at']

