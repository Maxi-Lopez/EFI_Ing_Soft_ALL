from django.urls import path, include
from .routers import router

app_name = 'wishlist'

urlpatterns = [
    path('', include(router.urls)),
]
