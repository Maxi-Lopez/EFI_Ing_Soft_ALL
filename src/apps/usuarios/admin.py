from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    model = Persona
    list_display = ['user', 'dni', 'telefono', 'fecha_nacimiento']
    list_filter = ['user__is_active', 'user__is_staff', 'user__date_joined']
    search_fields = ['user__username', 'user__email', 'dni']
    ordering = ['-user__date_joined']

    fieldsets = (
        ('Datos de cuenta', {
            'fields': ('user',),
        }),
        ('Datos personales', {
            'fields': ('dni', 'telefono', 'fecha_nacimiento', 'avatar_url'),
        }),
    )

    autocomplete_fields = ['user']
