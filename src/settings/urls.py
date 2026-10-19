from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),

    # JWT authentication
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    # Apps (descomentar a medida que se implementan)
    # path('api/v1/usuarios/', include('apps.usuarios.urls')),
    path('api/v1/catalogo/', include('apps.catalogo.urls')),
    # path('api/v1/carrito/', include('apps.carrito.urls')),
    # path('api/v1/ordenes/', include('apps.ordenes.urls')),
    # path('api/v1/pagos/', include('apps.pagos.urls')),
    # path('api/v1/envios/', include('apps.envios.urls')),
    # path('api/v1/promociones/', include('apps.promociones.urls')),
    # path('api/v1/wishlist/', include('apps.wishlist.urls')),
    # path('api/v1/reviews/', include('apps.reviews.urls')),
]
