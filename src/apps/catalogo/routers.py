from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r'categorias', api_views.CategoriaViewSet, basename='categorias')
router.register(r'marcas', api_views.MarcaViewSet, basename='marcas')
router.register(r'productos', api_views.ProductoViewSet, basename='productos')
router.register(
    r'imagenes', api_views.ProductoImagenViewSet, basename='imagenes'
)
router.register(
    r'especificaciones',
    api_views.EspecificacionViewSet,
    basename='especificaciones',
)
router.register(r'variantes', api_views.VarianteViewSet, basename='variantes')

urlpatterns = [
    path('', include(router.urls)),
]
