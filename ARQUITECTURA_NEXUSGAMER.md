# 🎮 NexusGamer - Arquitectura API REST (Educacional)

> **Tienda ficticia:** NexusGamer - "Tu portal al gaming next-gen"
> **Stack:** Django 6.1 + DRF + PostgreSQL + JWT + Next.js Frontend
> **Deploy target:** Supabase (PostgreSQL gratis) + Vercel (Next.js)
> **Estado:** Solo API - Sin checkout real, fines educativos

---

## 📐 Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        NEXUSGAMER API                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Auth    │  │ Catalogo │  │  Carrito │  │ Ordenes  │        │
│  │  (JWT)   │  │  (READ)  │  │ (SESSION)│  │  (CRUD)  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Usuarios │  │Promociones│ │  Pagos   │  │ Envios   │        │
│  │ (Profile)│  │ (READ)   │  │ (MOCK)   │  │ (CALC)   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
├─────────────────────────────────────────────────────────────────┤
│                    PostgreSQL (Supabase Ready)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelos de Datos (PostgreSQL)

### 1. **Auth & Usuarios** (User por defecto de Django + perfil `persona`)

```sql
-- auth_user (django.contrib.auth.models.User, tabla nativa de Django)
id, username, email, password, first_name, last_name,
is_staff, is_active, date_joined, last_login

-- persona (perfil 1:1, PK compartida con auth_user.id)
user_id (PK, FK -> auth_user.id),
dni, telefono, fecha_nacimiento, avatar_url

-- users_direccion
id, usuario_id (FK -> auth_user.id), alias, calle, numero, piso, dpto,
ciudad, provincia, codigo_postal, pais (default 'AR'),
es_predeterminada, latitud, longitud (para envíos)
```

### 2. **Catálogo** (Solo lectura pública)

```sql
-- catalogo_categoria
id, nombre, slug (unique), descripcion, imagen_url,
categoria_padre_id (FK self, nullable), orden, activa

-- catalogo_marca
id, nombre, slug (unique), logo_url, descripcion, pais_origen, activa

-- catalogo_producto
id, nombre, slug (unique), descripcion_corta, descripcion_larga (JSON/rich text),
sku (unique), precio_lista (DECIMAL 12,2), precio_oferta (nullable),
iva_porcentaje (default 21.00), stock_total, stock_reservado,
activo, destacado, fecha_lanzamiento,
marca_id (FK), categoria_id (FK),
created_at, updated_at

-- catalogo_productoimagen
id, producto_id (FK), imagen_url, alt_text, orden, es_principal

-- catalogo_especificacion (clave-valor tipado)
id, producto_id (FK), nombre, valor, tipo (text/number/boolean), unidad, orden

-- catalogo_variante (para productos con opciones: color, talle, storage)
id, producto_id (FK), sku_variante, nombre, precio_adicional,
stock, activa, atributos (JSONB: {"color": "negro", "storage": "1tb"})
```

### 3. **Carrito** (Persistente en BD)

```sql
-- carrito_carrito
id, usuario_id (FK nullable), session_key (char 40, nullable),
creado_en, actualizado_en
-- Constraint: usuario_id XOR session_key

-- carrito_item
id, carrito_id (FK), producto_id (FK), variante_id (FK nullable),
cantidad, precio_unitario_snapshot (DECIMAL), agregado_en
```

### 4. **Órdenes** (Simuladas - sin pago real)

```sql
-- ordenes_estadoorden (lookup table)
id, codigo (unique: 'pendiente', 'confirmado', 'preparando', 'enviado', 'entregado', 'cancelado'),
nombre, descripcion, orden, color_hex

-- ordenes_orden
id, numero_orden (unique, format: NG-2026-000001),
usuario_id (FK), estado_id (FK, default 'pendiente'),
subtotal, descuento_total, iva_total, envio_total, total_final,
direccion_envio (JSONB snapshot), metodo_envio_nombre, costo_envio,
metodo_pago_nombre, cuotas, codigo_cupon, descuento_cupon,
notas_cliente, notas_internas,
creada_en, confirmada_en, enviada_en, entregada_en, cancelada_en, cancelacion_motivo

-- ordenes_ordenitem
id, orden_id (FK), producto_id (FK), variante_id (FK nullable),
nombre_snapshot, sku_snapshot, precio_unitario, cantidad,
subtotal, iva_porcentaje, iva_monto

-- ordenes_historialestado
id, orden_id (FK), estado_anterior_id (FK nullable), estado_nuevo_id (FK),
usuario_id (FK nullable), notas, creado_en
```

### 5. **Promociones** (Read-only para frontend)

```sql
-- promociones_promocion
id, nombre, slug, descripcion, tipo (porcentaje/fijo/combo),
valor (DECIMAL), producto_ids (JSONB array), categoria_ids (JSONB),
marca_ids (JSONB), requiere_cupon, codigo_cupon (unique nullable),
fecha_inicio, fecha_fin, activa, max_usos_global, max_usos_usuario,
usos_actuales, aplica_envio_gratis, minimo_compra

-- promociones_ofertasemanal (landing page)
id, producto_id (FK), precio_oferta, fecha_inicio, fecha_fin,
posicion_homepage, activa
```

### 6. **Pagos** (Mock para demo)

```sql
-- pagos_metodopago
id, nombre, codigo (unique: 'mp_credito', 'mp_debito', 'mp_efectivo', 'transferencia'),
descripcion, activo, tiene_cuotas, max_cuotas, interes_cuotas (JSONB: {"3": 0, "6": 0, "12": 15})

-- pagos_pago (simulado)
id, orden_id (FK), metodo_pago_id (FK), monto, estado ('pendiente', 'aprobado', 'rechazado', 'reembolsado'),
cuotas, external_id (mercadopago_id mock), payload_respuesta (JSONB),
creado_en, aprobado_en
```

### 7. **Envíos** (Cálculo estimado)

```sql
-- envios_metodoenvio
id, nombre, codigo (unique: 'estandar', 'express', 'retiro'),
descripcion, costo_base, costo_por_km, gratis_desde_monto,
tiempo_estimado_min_dias, tiempo_estimado_max_dias, activo

-- envios_zonaenvio
id, nombre, provincia, codigo_postal_desde, codigo_postal_hasta,
factor_costo (multiplicador), activo

-- envios_envio
id, orden_id (FK), metodo_envio_id (FK), zona_id (FK),
costo_calculado, tracking_number (nullable), transportadora,
estado ('pendiente', 'despachado', 'en_transito', 'entregado', 'devuelto'),
despachado_en, entregado_en, payload_tracking (JSONB)
```

### 8. **Wishlist & Reviews**

```sql
-- wishlist_listadeseos
id, usuario_id (FK unique), creado_en, actualizado_en

-- wishlist_item
id, lista_id (FK), producto_id (FK), variante_id (FK nullable), agregado_en

-- reviews_resena
id, producto_id (FK), usuario_id (FK), orden_item_id (FK nullable, verified purchase),
puntuacion (1-5), titulo, comentario, verificada, util_count,
creada_en, actualizada_en

-- reviews_resenaimagen
id, resena_id (FK), imagen_url, orden
```

---

## 🔌 Endpoints API (v1)

### Auth (`/api/v1/auth/`)
```
POST   /auth/register/           # Registro + email verification (mock)
POST   /auth/login/              # JWT obtain (access + refresh)
POST   /auth/refresh/            # Refresh access token
POST   /auth/logout/             # Blacklist refresh token
GET    /auth/me/                 # Usuario actual + perfil
PUT    /auth/me/                 # Actualizar perfil
POST   /auth/password/change/    # Cambio password
POST   /auth/password/reset/     # Request reset (mock email)
POST   /auth/password/reset/confirm/  # Confirm reset
```

### Catálogo (`/api/v1/catalogo/`) - **Públicos (AllowAny)**
```
GET    /categorias/              # Tree structure ?nivel=1
GET    /categorias/{slug}/       # Detail + productos paginados
GET    /marcas/                  # List todas
GET    /marcas/{slug}/           # Detail + productos

GET    /productos/               # List con filtros avanzados
GET    /productos/{slug}/        # Detail completo (imágenes, specs, variantes, reviews)
GET    /productos/destacados/    # Homepage hero + grid
GET    /productos/novedades/     # Últimos 20 lanzamientos
GET    /productos/ofertas/       # Con precio_oferta vigente
GET    /productos/buscar/        # Full-text search ?q=rtx+4080

# Filtros query params:
# ?categoria=gpu&marca=asus&precio_min=100000&precio_max=500000
# &stock=disponible&ordenar=-fecha_lanzamiento&pagina=1&por_pagina=24
# &specs={"memoria": "16gb", "tipo": "gddr6"}
```

### Carrito (`/api/v1/carrito/`) - **Autenticado o Session**
```
GET    /carrito/                 # Obtener carrito (crea si no existe)
POST   /carrito/items/           # Agregar item
PATCH  /carrito/items/{id}/      # Actualizar cantidad
DELETE /carrito/items/{id}/      # Quitar item
DELETE /carrito/                 # Vaciar carrito
POST   /carrito/sync/            # Merge session cart → user cart (login)
```

### Órdenes (`/api/v1/ordenes/`) - **Autenticado**
```
POST   /ordenes/                 # Crear orden desde carrito (valida stock)
GET    /ordenes/                 # Listar mis órdenes (paginado, filtros estado)
GET    /ordenes/{numero}/        # Detalle orden + items + historial + tracking
POST   /ordenes/{numero}/cancelar/  # Cancelar si estado lo permite
```

### Promociones (`/api/v1/promociones/`) - **Públicos**
```
GET    /promociones/             # Activas vigentes
GET    /promociones/{slug}/      # Detail
POST   /promociones/validar/     # Validar cupón {codigo, carrito_items} → descuento
GET    /ofertas-semana/          # Landing page weekly deals
```

### Pagos (`/api/v1/pagos/`) - **Mock educacional**
```
POST   /pagos/iniciar/           # {orden_id, metodo_pago_id, cuotas} → {payment_id, mock_redirect_url}
GET    /pagos/{id}/              # Estado pago
POST   /pagos/webhook/           # Mock MercadoPago IPN (para testing)
```

### Envíos (`/api/v1/envios/`)
```
POST   /envios/calcular/         # {codigo_postal, items[]} → {metodos_disponibles[]}
GET    /envios/{tracking}/tracking/  # Mock tracking info
```

### Usuario (`/api/v1/usuarios/`) - **Autenticado**
```
GET    /usuarios/perfil/         # Perfil completo
PUT    /usuarios/perfil/         # Actualizar
GET    /usuarios/direcciones/    # List
POST   /usuarios/direcciones/    # Crear
PUT    /usuarios/direcciones/{id}/
DELETE /usuarios/direcciones/{id}/
POST   /usuarios/direcciones/{id}/predeterminada/
```

### Wishlist (`/api/v1/wishlist/`) - **Autenticado**
```
GET    /wishlist/                # Mi lista
POST   /wishlist/                # Agregar
DELETE /wishlist/{producto_id}/  # Quitar
```

### Reviews (`/api/v1/reviews/`)
```
GET    /productos/{producto_id}/reviews/  # Paginado, filtros puntuación
POST   /productos/{producto_id}/reviews/  # Crear (solo verified purchase)
POST   /reviews/{id}/util/         # Marcar útil
```

---

## 🔐 Permisos & Autenticación

| Endpoint | Permiso | Throttle |
|----------|---------|----------|
| `/auth/*` | `AllowAny` | `UserRateThrottle` (10/min) |
| `/catalogo/*` | `AllowAny` | `AnonRateThrottle` (100/min) |
| `/promociones/*` | `AllowAny` | `AnonRateThrottle` |
| `/carrito/*` | `IsAuthenticatedOrSession` | `UserRateThrottle` |
| `/ordenes/*` | `IsOwnerOrReadOnly` | `UserRateThrottle` |
| `/pagos/*` | `IsAuthenticated` | `UserRateThrottle` (5/min) |
| `/usuarios/*` | `IsAuthenticated` | `UserRateThrottle` |
| `/wishlist/*` | `IsAuthenticated` | `UserRateThrottle` |
| `/reviews/* (GET)` | `AllowAny` | `AnonRateThrottle` |
| `/reviews/* (POST)` | `IsAuthenticated + VerifiedPurchase` | `UserRateThrottle` |

**JWT Settings:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

## ⚙️ Configuración Django (Supabase Ready)

### Settings clave
```python
# database - Supabase connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),  # db.xxx.supabase.co
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': 10,
        },
    }
}

# Cache - Redis (Upstash gratis para Supabase)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'nexusgamer',
    }
}

# Media files - Supabase Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = env('SUPABASE_STORAGE_URL')
AWS_ACCESS_KEY_ID = env('SUPABASE_STORAGE_KEY')
AWS_SECRET_ACCESS_KEY = env('SUPABASE_STORAGE_SECRET')
AWS_STORAGE_BUCKET_NAME = 'nexusgamer-media'
AWS_S3_REGION_NAME = 'auto'
AWS_QUERYSTRING_AUTH = False
```

### Paquetes requeridos (`requirements.txt`)
```
Django>=6.1,<7.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-filter>=23.5
drf-spectacular>=0.27  # OpenAPI 3
django-cors-headers>=4.4
python-dotenv>=1.0
psycopg2-binary>=2.9
django-storages>=1.14
boto3>=1.34
redis>=5.0
django-redis>=5.4
gunicorn>=21.0
```

---

## 📁 Estructura de Apps Django

```
nexusgamer/
├── config/                 # Settings, URLs root, WSGI/ASGI
├── apps/
│   ├── core/               # Abstract models, mixins, utilities
│   ├── users/              # Custom user, perfiles, direcciones
│   ├── catalogo/           # Categorías, marcas, productos, specs
│   ├── carrito/            # Carrito persistente
│   ├── ordenes/            # Órdenes, items, estados
│   ├── pagos/              # Métodos, pagos (mock)
│   ├── envios/             # Métodos, zonas, cálculo
│   ├── promociones/        # Promos, cupones, ofertas semanales
│   ├── wishlist/           # Lista de deseos
│   └── reviews/            # Reseñas, imágenes
├── static/                 # Collectstatic
├── media/                  # Local dev only
├── tests/                  # Test suite global
├── scripts/                # Seed data, migraciones custom
└── manage.py
```

---

## 🌱 Seed Data (Para desarrollo)

```python
# scripts/seed.py - Ejecutar post-migración
- 10 Categorías (GPUs, CPUs, Motherboards, RAM, Storage, Monitores, Periféricos, Sillas, Consolas, Accesorios)
- 15 Marcas (ASUS, MSI, Gigabyte, AMD, Intel, NVIDIA, Corsair, Razer, Logitech, Samsung, LG, Kingston, WD, Seagate, Cooler Master)
- 50+ Productos con imágenes placeholder, specs realistas, variantes
- 5 Promociones activas (Black Friday, Cyber Monday, Hot Sale, etc.)
- 3 Métodos de pago (MercadoPago Crédito/Débito/Efectivo, Transferencia)
- 3 Métodos de envío (Estándar, Express, Retiro en sucursal)
- 24 Zonas de envío (provincias AR con factores de costo)
- Estados de orden predefinidos
- Usuario admin + 3 usuarios test
```

---

## 🧪 Testing Strategy

| Tipo | Herramienta | Cobertura objetivo |
|------|-------------|-------------------|
| Unit | `pytest` + `factory_boy` | Models, serializers, services > 80% |
| Integration | `pytest-django` | Views, permissions, filters |
| API Contract | `schemathesis` | OpenAPI spec validation |
| E2E (Mock) | `playwright` (opcional) | Flows: browse → cart → order |

---

## 📦 Deploy Checklist (Supabase + Vercel)

### Supabase (PostgreSQL + Storage + Auth opcional)
- [ ] Crear proyecto Supabase
- [ ] Configurar connection pooling (PgBouncer)
- [ ] Crear bucket `nexusgamer-media` (public read)
- [ ] Ejecutar migraciones Django
- [ ] Poblar seed data
- [ ] Configurar RLS policies si se usa Supabase Auth

### Backend (Railway/Render/Fly.io - gratis tier)
- [ ] Build Docker image multi-stage
- [ ] Configurar vars de entorno
- [ ] Health check endpoint `/health/`
- [ ] Static files → WhiteNoise o CDN
- [ ] Logs estructurados (JSON)

### Frontend Next.js (Vercel)
- [ ] `next.config.js` con `images.remotePatterns` para Supabase Storage
- [ ] API client (TanStack Query + Axios/Fetch)
- [ ] Auth context (JWT en httpOnly cookies)
- [ ] Carrito persistente (localStorage + sync)
- [ ] SSR/ISR para catálogo (SEO)

---

## 🎯 Próximos Pasos (Orden sugerido)

1. **Setup inicial**
   - [ ] Crear proyecto Django con estructura `apps/`
   - [ ] Configurar perfil `persona` (1:1 con User de Django) + migraciones iniciales
   - [ ] Setup `drf-spectacular` + Swagger UI
   - [ ] Configurar CORS para `localhost:3000` (Next.js)

2. **Catálogo (Core público)**
   - [ ] Models: Categoria, Marca, Producto, Imagen, Especificacion, Variante
   - [ ] Serializers con nested relations
   - [ ] ViewSets + `django-filter` avanzado
   - [ ] Paginación personalizada + ordering
   - [ ] Seed data realista (50+ productos gaming)

3. **Auth + Usuario**
   - [ ] JWT endpoints personalizados
   - [ ] Perfil + Direcciones CRUD
   - [ ] Permisos `IsOwnerOrReadOnly`

4. **Carrito + Órdenes**
   - [ ] Carrito persistente (user + session)
   - [ ] Checkout flow: carrito → orden (snapshot precios/stock)
   - [ ] Validación stock atómico (SELECT FOR UPDATE)

5. **Pagos + Envíos (Mock)**
   - [ ] Métodos de pago con cuotas
   - [ ] Cálculo envío por zona/CP
   - [ ] Webhook mock para testing

6. **Promociones + Wishlist + Reviews**
   - [ ] Cupón validation endpoint
   - [ ] Ofertas semanales homepage
   - [ ] Wishlist toggle
   - [ ] Reviews solo verified purchase

7. **Performance + Observabilidad**
   - [ ] Redis cache para listings
   - [ ] Database indexes (GIN para JSONB specs, trigram para search)
   - [ ] Logging estructurado + Sentry (gratis)
   - [ ] Rate limiting diferenciado

8. **Documentación + DX**
   - [ ] OpenAPI spec completa
   - [ ] Postman collection export
   - [ ] README con setup local + deploy

---

## 💡 Decisiones de Diseño Clave

| Decisión | Razón |
|----------|-------|
| **User por defecto + perfil `persona`** | `auth_user` de Django + tabla `persona` 1:1 (dni, teléfono, avatar) |
| **JSONB para specs/atributos** | Esquema flexible tipo NoSQL en Postgres |
| **Snapshot precios en orden/item** | Inmutabilidad histórica, auditoría |
| **Carrito dual (user + session)** | UX sin login + merge al loguear |
| **Estados de orden como tabla lookup** | Extensible, i18n-ready, ordenable |
| **Promociones genéricas (JSONB targets)** | Flexible: por producto, categoría, marca, combo |
| **Pagos mock** | Educacional sin credenciales reales |
| **Supabase Storage** | Gratis 1GB, CDN global, S3-compatible |

---

## 📚 Recursos de Referencia

- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [django-filter](https://django-filter.readthedocs.io/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Supabase Django Guide](https://supabase.com/docs/guides/getting-started/tutorials/with-django)
- [CompraGamer UX patterns](https://compragamer.com/) (referencia visual)

---

> **Nota:** Este documento es la especificación técnica completa. La implementación se hará en fases, priorizando catálogo + auth + carrito + órdenes como MVP funcional para el frontend Next.js.