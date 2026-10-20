from rest_framework import serializers

from .models import (
    Categoria,
    Especificacion,
    Marca,
    Producto,
    ProductoImagen,
    Variante,
)


# ============================================================================
# Serializadores PÚBLICOS (solo lectura, relaciones anidadas)
# ============================================================================

class CategoriaPublicSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField(read_only=True)
    nivel = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'imagen_url',
            'categoria_padre', 'subcategorias', 'nivel', 'orden',
            'activa', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subcategorias(self, obj):
        if obj.subcategorias.exists():
            return CategoriaPublicSerializer(
                obj.subcategorias.filter(activa=True), many=True
            ).data
        return []

    def get_nivel(self, obj):
        return obj.nivel


class MarcaPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'slug', 'logo_url', 'descripcion',
            'pais_origen', 'activa', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VariantePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = [
            'id', 'sku_variante', 'nombre', 'precio_adicional',
            'stock', 'activa', 'atributos', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductoImagenPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = [
            'id', 'imagen_url', 'alt_text', 'orden', 'es_principal',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class EspecificacionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especificacion
        fields = [
            'id', 'nombre', 'valor', 'tipo', 'unidad', 'orden',
        ]
        read_only_fields = ['id']


class ProductoPublicSerializer(serializers.ModelSerializer):
    """Producto con relaciones anidadas (solo lectura)."""
    marca = MarcaPublicSerializer(read_only=True)
    categoria = CategoriaPublicSerializer(read_only=True)
    imagenes = ProductoImagenPublicSerializer(many=True, read_only=True)
    especificaciones = EspecificacionPublicSerializer(
        many=True, read_only=True
    )
    variantes = VariantePublicSerializer(
        many=True, read_only=True
    )
    precio_final = serializers.SerializerMethodField(read_only=True)
    stock_disponible = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'slug', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta', 'precio_final',
            'iva_porcentaje', 'stock_total', 'stock_reservado',
            'stock_disponible', 'activo', 'destacado', 'fecha_lanzamiento',
            'marca', 'categoria', 'imagenes', 'especificaciones',
            'variantes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_precio_final(self, obj):
        return obj.precio_oferta if obj.precio_oferta else obj.precio_lista

    def get_stock_disponible(self, obj):
        return obj.stock_disponible


# ============================================================================
# Serializadores DE ESCRITURA (FKs por ID plano)
# ============================================================================

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'imagen_url',
            'categoria_padre', 'orden', 'activa',
        ]
        read_only_fields = ['id']


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'slug', 'logo_url', 'descripcion',
            'pais_origen', 'activa',
        ]
        read_only_fields = ['id']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'slug', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta', 'iva_porcentaje',
            'stock_total', 'stock_reservado', 'activo', 'destacado',
            'fecha_lanzamiento', 'marca', 'categoria',
        ]
        read_only_fields = ['id']


class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = [
            'id', 'producto', 'imagen_url', 'alt_text',
            'orden', 'es_principal',
        ]
        read_only_fields = ['id']


class EspecificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especificacion
        fields = [
            'id', 'producto', 'nombre', 'valor', 'tipo', 'unidad', 'orden',
        ]
        read_only_fields = ['id']


class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = [
            'id', 'producto', 'sku_variante', 'nombre', 'precio_adicional',
            'stock', 'activa', 'atributos',
        ]
        read_only_fields = ['id']
