from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r'carrito', api_views.CarritoViewSet, basename='carrito')
router.register(r'items', api_views.CarritoItemViewSet, basename='carrito-items')

urlpatterns = [
    path('', include(router.urls)),
]
