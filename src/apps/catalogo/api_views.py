from django.db import models
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Categoria,
    Especificacion,
    Marca,
    Producto,
    ProductoImagen,
    Variante,
)
from .serializers import (
    CategoriaPublicSerializer,
    CategoriaSerializer,
    EspecificacionPublicSerializer,
    EspecificacionSerializer,
    MarcaPublicSerializer,
    MarcaSerializer,
    ProductoImagenPublicSerializer,
    ProductoImagenSerializer,
    ProductoPublicSerializer,
    ProductoSerializer,
    VariantePublicSerializer,
    VarianteSerializer,
)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """Categorías públicas (solo lectura)."""

    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaPublicSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'orden', 'created_at']
    ordering = ['orden', 'nombre']

    def get_queryset(self):
        qs = super().get_queryset()
        nivel = self.request.query_params.get('nivel')
        if nivel is not None:
            try:
                nivel_int = int(nivel)
                if nivel_int == 1:
                    qs = qs.filter(categoria_padre__isnull=True)
                else:
                    qs = qs.filter(categoria_padre__isnull=False)
            except ValueError:
                pass
        return qs


class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    """Marcas públicas (solo lectura)."""

    queryset = Marca.objects.filter(activa=True)
    serializer_class = MarcaPublicSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['nombre', 'pais_origen']
    ordering_fields = ['nombre', 'pais_origen']
    ordering = ['nombre']


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """Productos públicos con filtros, búsqueda y paginación."""

    queryset = Producto.objects.filter(activo=True).select_related(
        'marca', 'categoria'
    )
    serializer_class = ProductoPublicSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        'categoria__slug': ['exact'],
        'marca__slug': ['exact'],
        'precio_lista': ['gte', 'lte'],
        'precio_oferta': ['gte', 'lte'],
        'stock_total': ['gte'],
        'destacado': ['exact'],
        'activo': ['exact'],
    }
    search_fields = ['nombre', 'sku', 'descripcion_corta']
    ordering_fields = [
        'nombre', 'precio_lista', 'precio_oferta',
        'stock_total', 'fecha_lanzamiento', 'created_at',
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()

        # Filtro de stock disponible
        stock_disponible = self.request.query_params.get('stock_disponible')
        if stock_disponible == 'true':
            qs = qs.filter(stock_total__gt=models.F('stock_reservado'))
        elif stock_disponible == 'false':
            qs = qs.filter(stock_total__lte=models.F('stock_reservado'))

        # Precio mínimo/máximo (considerando oferta)
        precio_min = self.request.query_params.get('precio_min')
        precio_max = self.request.query_params.get('precio_max')
        if precio_min:
            qs = qs.filter(
                Q(precio_oferta__isnull=False, precio_oferta__gte=precio_min)
                | Q(precio_oferta__isnull=True, precio_lista__gte=precio_min)
            )
        if precio_max:
            qs = qs.filter(
                Q(precio_oferta__isnull=False, precio_oferta__lte=precio_max)
                | Q(precio_oferta__isnull=True, precio_lista__lte=precio_max)
            )

        return qs.distinct()

    @action(detail=False, methods=['get'], url_path='destacados')
    def destacados(self, request):
        """Productos destacados para homepage hero + grid."""
        qs = self.get_queryset().filter(destacado=True)[:24]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='novedades')
    def novedades(self, request):
        """Últimos 20 lanzamientos."""
        qs = self.get_queryset().exclude(
            fecha_lanzamiento__isnull=True
        ).order_by('-fecha_lanzamiento')[:20]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='ofertas')
    def ofertas(self, request):
        """Productos con precio de oferta vigente."""
        qs = self.get_queryset().filter(precio_oferta__isnull=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='buscar')
    def buscar(self, request):
        """Búsqueda full-text por query q."""
        q = request.query_params.get('q', '')
        if not q:
            return Response({'resultados': [], 'count': 0})
        qs = self.get_queryset().filter(
            Q(nombre__icontains=q)
            | Q(sku__icontains=q)
            | Q(descripcion_corta__icontains=q)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ProductoImagenViewSet(viewsets.ReadOnlyModelViewSet):
    """Imágenes de productos públicas."""

    queryset = ProductoImagen.objects.all().select_related('producto')
    serializer_class = ProductoImagenPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['producto', 'es_principal']
    ordering_fields = ['orden', 'created_at']
    ordering = ['orden', 'id']


class EspecificacionViewSet(viewsets.ReadOnlyModelViewSet):
    """Especificaciones de productos públicas."""

    queryset = Especificacion.objects.all().select_related('producto')
    serializer_class = EspecificacionPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['producto', 'tipo']
    ordering_fields = ['orden', 'nombre']
    ordering = ['orden', 'nombre']


class VarianteViewSet(viewsets.ReadOnlyModelViewSet):
    """Variantes de productos públicas."""

    queryset = Variante.objects.filter(activa=True).select_related('producto')
    serializer_class = VariantePublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['producto', 'activa']
    ordering_fields = ['nombre', 'precio_adicional', 'stock']
    ordering = ['nombre']
