from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from apps.base import NoDeleteModalAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin, NoDeleteModalAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Assistent Info'), {'fields': ('wechat_no', 'url_qr_code_wx', 'telephone')}),
    )


@admin.register(Permission)
class PermissionAdmin(NoDeleteModalAdmin):
    pass
