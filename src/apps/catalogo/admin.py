from django.contrib import admin

from .models import (
    Categoria,
    Especificacion,
    Marca,
    Producto,
    ProductoImagen,
    Variante,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'categoria_padre', 'nivel', 'orden', 'activa']
    list_filter = ['activa', 'categoria_padre']
    search_fields = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['orden', 'nombre']
    list_editable = ['orden', 'activa']

    def nivel(self, obj):
        return obj.nivel


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'pais_origen', 'activa']
    list_filter = ['activa', 'pais_origen']
    search_fields = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['nombre']
    list_editable = ['activa']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'slug', 'sku', 'marca', 'categoria',
        'precio_lista', 'precio_oferta', 'stock_total',
        'activo', 'destacado',
    ]
    list_filter = ['activo', 'destacado', 'marca', 'categoria']
    search_fields = ['nombre', 'sku', 'descripcion_corta']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['-created_at']
    list_editable = ['activo', 'destacado', 'precio_oferta']
    autocomplete_fields = ['marca', 'categoria']


@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ['producto', 'alt_text', 'orden', 'es_principal']
    list_filter = ['es_principal']
    search_fields = ['producto__nombre', 'alt_text']
    ordering = ['orden', 'id']
    autocomplete_fields = ['producto']


@admin.register(Especificacion)
class EspecificacionAdmin(admin.ModelAdmin):
    list_display = ['producto', 'nombre', 'valor', 'tipo', 'unidad', 'orden']
    list_filter = ['tipo', 'unidad']
    search_fields = ['producto__nombre', 'nombre', 'valor']
    ordering = ['orden', 'nombre']
    autocomplete_fields = ['producto']


@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    list_display = ['sku_variante', 'nombre', 'producto', 'precio_adicional', 'stock', 'activa']
    list_filter = ['activa']
    search_fields = ['sku_variante', 'nombre', 'producto__nombre']
    ordering = ['nombre']
    autocomplete_fields = ['producto']
