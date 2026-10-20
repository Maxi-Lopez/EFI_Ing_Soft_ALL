from django.contrib import admin

from .models import Carrito, CarritoItem


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'session_key', 'actualizado_en']
    list_filter = ['usuario', 'creado_en', 'actualizado_en']
    search_fields = ['usuario__username', 'session_key']
    ordering = ['-actualizado_en']
    autocomplete_fields = ['usuario']


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = [
        'producto', 'variante', 'carrito', 'cantidad',
        'precio_unitario_snapshot', 'agregado_en',
    ]
    list_filter = ['agregado_en', 'carrito__usuario']
    search_fields = [
        'producto__nombre', 'carrito__usuario__username',
    ]
    ordering = ['-agregado_en']
    autocomplete_fields = ['producto', 'variante', 'carrito']
