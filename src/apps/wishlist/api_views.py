from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ItemListaDeseos, ListaDeseos
from .serializers import (
    ItemListaDeseosPublicSerializer,
    ItemListaDeseosSerializer,
)


class ItemListaDeseosViewSet(viewsets.ModelViewSet):
    """Items de la lista de deseos del usuario autenticado."""

    serializer_class = ItemListaDeseosSerializer
    serializer_action_classes = {
        'list': ItemListaDeseosPublicSerializer,
        'retrieve': ItemListaDeseosPublicSerializer,
    }
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return ItemListaDeseos.objects.filter(
            lista__usuario=self.request.user
        ).select_related('producto', 'variante', 'lista')

    def get_serializer_class(self):
        return self.serializer_action_classes.get(
            self.action, self.serializer_class
        )

    def perform_create(self, serializer):
        lista, _ = ListaDeseos.objects.get_or_create(
            usuario=self.request.user
        )
        serializer.save(lista=lista)

    @action(detail=False, methods=['delete'], url_path='limpiar')
    def limpiar(self, request):
        """Vacía toda la lista de deseos del usuario."""
        self.get_queryset().delete()
        return Response(
            {'mensaje': 'Lista de deseos vaciada'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle(self, request):
        """Agrega o quita un producto de la lista de deseos."""
        producto_id = request.data.get('producto')
        variante_id = request.data.get('variante')

        if not producto_id:
            return Response(
                {'error': 'producto es requerido'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lista, _ = ListaDeseos.objects.get_or_create(
            usuario=request.user
        )

        filtros = {'lista': lista, 'producto_id': producto_id}
        if variante_id:
            filtros['variante_id'] = variante_id
        else:
            filtros['variante__isnull'] = True

        existe = ItemListaDeseos.objects.filter(**filtros).exists()
        if existe:
            ItemListaDeseos.objects.filter(**filtros).delete()
            return Response(
                {'mensaje': 'Producto removido de la lista de deseos'},
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = self.get_serializer(
            data={'producto': producto_id, 'variante': variante_id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
