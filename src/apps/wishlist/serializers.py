from rest_framework import serializers

from apps.catalogo.serializers import (
    ProductoPublicSerializer,
    VariantePublicSerializer,
)

from .models import ItemListaDeseos, ListaDeseos


# ============================================================================
# Serializadores PÚBLICOS (solo lectura, relaciones anidadas)
# ============================================================================

class ItemListaDeseosPublicSerializer(serializers.ModelSerializer):
    """Item de lista de deseos con producto y variante anidados (solo lectura)."""

    producto = ProductoPublicSerializer(read_only=True)
    variante = VariantePublicSerializer(read_only=True)

    class Meta:
        model = ItemListaDeseos
        fields = [
            'id', 'producto', 'variante', 'agregado_en',
        ]
        read_only_fields = ['id', 'agregado_en']


class ListaDeseosPublicSerializer(serializers.ModelSerializer):
    """Lista de deseos con sus items anidados (solo lectura)."""

    items = ItemListaDeseosPublicSerializer(many=True, read_only=True)

    class Meta:
        model = ListaDeseos
        fields = [
            'id', 'usuario', 'items', 'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']


# ============================================================================
# Serializadores DE ESCRITURA (FKs por ID plano)
# ============================================================================

class ItemListaDeseosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemListaDeseos
        fields = [
            'id', 'lista', 'producto', 'variante',
        ]
        read_only_fields = ['id', 'lista']


class ListaDeseosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaDeseos
        fields = [
            'id', 'usuario',
        ]
        read_only_fields = ['id']
