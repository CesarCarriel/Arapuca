from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models.user import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Informações pessoais', {'fields': ('name', 'password', 'email', 'phone')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('name', 'email', 'phone')
    list_display = ('id', 'name', 'phone', 'email', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('id',)
