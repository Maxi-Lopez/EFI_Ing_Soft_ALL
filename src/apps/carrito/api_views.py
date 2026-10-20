from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Carrito, CarritoItem
from .serializers import (
    CarritoItemSerializer,
    CarritoItemPublicSerializer,
    CarritoPublicSerializer,
)


def _precio_unitario(producto, variante=None):
    """Calcula el precio unitario snapshot (oferta > lista + variante adicional)."""
    base = producto.precio_oferta if producto.precio_oferta else producto.precio_lista
    if variante and variante.precio_adicional:
        base += variante.precio_adicional
    return base


class CarritoViewSet(viewsets.GenericViewSet):
    """Carrito de compras del usuario autenticado (único por usuario)."""

    serializer_class = CarritoPublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrito.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action == 'items':
            return CarritoItemPublicSerializer
        return CarritoPublicSerializer

    @action(detail=False, methods=['get'], url_path='mi-carrito')
    def mi_carrito(self, request):
        """Obtiene el carrito del usuario (lo crea si no existe)."""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        serializer = self.get_serializer(carrito)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='vaciar')
    def vaciar(self, request):
        """Vacía el carrito del usuario (borra todos los ítems)."""
        self.get_queryset().prefetch_related('items').all()
        CarritoItem.objects.filter(
            carrito__usuario=request.user
        ).delete()
        return Response(
            {'mensaje': 'Carrito vaciado'},
            status=status.HTTP_204_NO_CONTENT,
        )


class CarritoItemViewSet(viewsets.ModelViewSet):
    """Ítems del carrito del usuario autenticado."""

    serializer_class = CarritoItemSerializer
    serializer_action_classes = {
        'list': CarritoItemPublicSerializer,
        'retrieve': CarritoItemPublicSerializer,
    }
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return CarritoItem.objects.filter(
            carrito__usuario=self.request.user
        ).select_related('producto', 'variante', 'carrito')

    def get_serializer_class(self):
        return self.serializer_action_classes.get(
            self.action, self.serializer_class
        )

    def perform_create(self, serializer):
        carrito, _ = Carrito.objects.get_or_create(
            usuario=self.request.user
        )
        producto = serializer.validated_data['producto']
        variante = serializer.validated_data.get('variante')
        serializer.save(
            carrito=carrito,
            precio_unitario_snapshot=_precio_unitario(producto, variante),
        )

    def perform_update(self, serializer):
        # Solo se puede actualizar la cantidad; el precio snapshot se mantiene
        serializer.save()

    @action(detail=False, methods=['post'], url_path='agregar')
    def agregar(self, request):
        """Agrega un producto al carrito (o incrementa cantidad si ya existe)."""
        producto_id = request.data.get('producto')
        variante_id = request.data.get('variante')
        cantidad = int(request.data.get('cantidad', 1))

        if not producto_id:
            return Response(
                {'error': 'producto es requerido'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        carrito, _ = Carrito.objects.get_or_create(
            usuario=request.user
        )

        filtros = {
            'carrito': carrito,
            'producto_id': producto_id,
        }
        if variante_id:
            filtros['variante_id'] = variante_id
        else:
            filtros['variante__isnull'] = True

        item = CarritoItem.objects.filter(**filtros).first()
        if item:
            item.cantidad += cantidad
            item.save()
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            data={
                'producto': producto_id,
                'variante': variante_id,
                'cantidad': cantidad,
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
