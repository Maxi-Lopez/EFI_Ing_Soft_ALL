from rest_framework import serializers

from apps.catalogo.serializers import (
    ProductoPublicSerializer,
    VariantePublicSerializer,
)

from .models import Carrito, CarritoItem


# ============================================================================
# Serializadores PÚBLICOS (solo lectura, relaciones anidadas)
# ============================================================================

class CarritoItemPublicSerializer(serializers.ModelSerializer):
    """Ítem de carrito con producto y variante anidados (solo lectura)."""

    producto = ProductoPublicSerializer(read_only=True)
    variante = VariantePublicSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CarritoItem
        fields = [
            'id', 'producto', 'variante', 'cantidad',
            'precio_unitario_snapshot', 'subtotal', 'agregado_en',
        ]
        read_only_fields = ['id', 'agregado_en']

    def get_subtotal(self, obj):
        return obj.subtotal


class CarritoPublicSerializer(serializers.ModelSerializer):
    """Carrito con sus ítems anidados (solo lectura)."""

    items = CarritoItemPublicSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Carrito
        fields = [
            'id', 'usuario', 'session_key', 'items', 'total',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def get_total(self, obj):
        return sum(item.subtotal for item in obj.items.all())


# ============================================================================
# Serializadores DE ESCRITURA (FKs por ID plano)
# ============================================================================

class CarritoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoItem
        fields = [
            'id', 'carrito', 'producto', 'variante', 'cantidad',
            'precio_unitario_snapshot',
        ]
        read_only_fields = ['id', 'carrito', 'precio_unitario_snapshot']


class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = [
            'id', 'usuario', 'session_key',
        ]
        read_only_fields = ['id']
