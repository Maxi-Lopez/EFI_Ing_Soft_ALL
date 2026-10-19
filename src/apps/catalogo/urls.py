from django.urls import path, include
from .routers import router
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', include(router.urls)),
    path('inicio/', views.inicio, name='inicio'),
]
