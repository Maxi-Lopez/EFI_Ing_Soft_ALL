from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'dni', 'telefono', 'is_staff', 'is_active',
    ]
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'dni', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Datos personales', {
            'fields': ('dni', 'telefono', 'fecha_nacimiento', 'avatar_url'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos personales', {
            'fields': ('dni', 'telefono', 'fecha_nacimiento', 'avatar_url'),
        }),
    )
