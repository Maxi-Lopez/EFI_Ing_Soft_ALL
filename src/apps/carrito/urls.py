from django.urls import path, include
from .routers import router

app_name = 'carrito'

urlpatterns = [
    path('', include(router.urls)),
]
