from django.contrib import admin

from .models import ItemListaDeseos, ListaDeseos


@admin.register(ListaDeseos)
class ListaDeseosAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'creado_en', 'actualizado_en']
    search_fields = ['usuario__username', 'usuario__email']
    ordering = ['-creado_en']


@admin.register(ItemListaDeseos)
class ItemListaDeseosAdmin(admin.ModelAdmin):
    list_display = ['producto', 'variante', 'lista__usuario', 'agregado_en']
    list_filter = ['agregado_en']
    search_fields = [
        'producto__nombre',
        'lista__usuario__username',
    ]
    ordering = ['-agregado_en']
    autocomplete_fields = ['producto', 'variante']
