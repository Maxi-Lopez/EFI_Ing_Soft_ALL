# 🎮 NexusGamer API

> **Tienda ficticia de gaming** — API REST desarrollada con Django 6.1 + Django REST Framework para el curso de Ingeniería de Software (EFI).

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-green?logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.18-red?logo=django)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://postgresql.org)
[![uv](https://img.shields.io/badge/uv-latest-orange?logo=uv)](https://github.com/astral-sh/uv)
[![JWT](https://img.shields.io/badge/Auth-JWT-purple)](https://django-rest-framework-simplejwt.readthedocs.io)
[![Swagger](https://img.shields.io/badge/Docs-Swagger-blue?logo=swagger)](https://drf-spectacular.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Tabla de contenidos

- [🎮 NexusGamer API](#-nexusgamer-api)
- [📋 Tabla de contenidos](#-tabla-de-contenidos)
- [📖 Sobre el proyecto](#-sobre-el-proyecto)
- [🛠️ Stack tecnológico](#-stack-tecnológico)
- [🏗️ Arquitectura](#-arquitectura)
- [📁 Estructura de carpetas](#-estructura-de-carpetas)
- [🗄️ Modelo de datos (Catálogo)](#-modelo-de-datos-catálogo)
- [🔌 Endpoints API](#-endpoints-api)
- [✅ Requisitos académicos cumplidos](#-requisitos-académicos-cumplidos)
- [🚀 Instalación y ejecución](#-instalación-y-ejecución)
- [⚙️ Variables de entorno](#-variables-de-entorno)
- [🗺️ Plan de trabajo por fases](#-plan-de-trabajo-por-fases)
- [👥 Equipo](#-equipo)
- [📸 Capturas del proyecto](#-capturas-del-proyecto)
- [📄 Licencia](#-licencia)

---

## 📖 Sobre el proyecto

**NexusGamer** es una API REST de una tienda de productos gaming diseñada para consumirse desde un frontend (Next.js, React, etc.). El sistema permite navegar por un catálogo de productos, autenticar usuarios, gestionar carritos de compra, crear órdenes, validar promociones y más.

Este proyecto se desarrolla como trabajo práctico para la materia **Ingeniería de Software (EFI)** y cumple con todos los requisitos académicos definidos en `requisitos.md`.

### Alcance actual (MVP)

| Componente | Estado |
|------------|--------|
| Setup del proyecto (Django, DRF, uv, PostgreSQL) | ✅ Completado |
| User por defecto de Django + perfil `persona` + Autenticación JWT | ✅ Completado (base) |
| App `catalogo` — 6 modelos, públicos, read-only | ✅ Completado |
| Filtros, búsqueda, paginación, nested serializers | ✅ Completado |
| 4 acciones custom (`@action`) | ✅ Completado |
| Admin de Django con filtros y búsqueda | ✅ Completado |
| Vista principal con template de bienvenida | ✅ Completado |
| Swagger / Redoc / OpenAPI 3 | ✅ Completado |
| CORS para frontend (`localhost:3000`) | ✅ Completado |
| App wishlist — lista de deseos por usuario | ✅ Completado |
| Apps restantes (carrito, órdenes, pagos, reviews) | ⏳ Pendiente |
| Docker + Despliegue | ⏳ Pendiente |

---

## 🛠️ Stack tecnológico

| Capa | Tecnología | Versión |
|------|------------|---------|
| Lenguaje | Python | 3.14 |
| Framework web | Django | 6.1 |
| API REST | Django REST Framework | 3.18 |
| Autenticación | SimpleJWT | 5.5 |
| Base de datos | PostgreSQL | 15+ |
| Gestor de paquetes | uv | latest |
| Filtros y búsqueda | django-filter | 26.2 |
| Documentación | drf-spectacular (OpenAPI 3) | 0.30 |
| CORS | django-cors-headers | 4.9 |
| Variables de entorno | django-environ | 0.14 |
| Cache | Redis / django-redis | 7.0 |
| Almacenamiento | django-storages + boto3 (S3/Supabase) | 1.14 |
| Servidor WSGI | gunicorn | 26.2 |

---

## 🏗️ Arquitectura

El proyecto sigue una arquitectura modular basada en apps de Django, separando responsabilidades por dominio de negocio.

```
┌─────────────────────────────────────────────────────────────────┐
│                        NEXUSGAMER API                           │
├──────────┬──────────┬──────────┬──────────┬──────────┬────────┤
│  Auth    │ Catalogo │ Carrito  │ Ordenes  │ Pagos    │ Envios │
│  (JWT)   │ (READ)   │ (SESSION)│ (CRUD)   │ (MOCK)   │ (CALC) │
├──────────┼──────────┼──────────┼──────────┼──────────┼────────┤
│ Usuarios │ Promos   │ Wishlist │ Reviews  │ Core     │        │
│ (Profile)│ (READ)   │          │          │          │        │
└──────────┴──────────┴──────────┴──────────┴──────────┴────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   PostgreSQL (Supabase)│
              │      + Redis Cache     │
              └────────────────────────┘
```

### Principios de diseño

- **Perfil `persona`**: tabla 1:1 con el `User` por defecto de Django (`auth_user`), PK compartida (`user_id`), campos DNI, teléfono, fecha de nacimiento y avatar.
- **Serializers duales**: serializer público (anidado, solo lectura) y serializer de escritura (FKs plano por ID).
- **Snapshots**: precios y stock se congelan en los ítems de orden para inmutabilidad histórica.
- **Soft delete**: los registros no se borran, se desactivan con campo `activo`/`activa`.
- **Pagos y envíos mock**: educacional, sin credenciales reales.

---

## 📁 Estructura de carpetas

```
nexusgamer/
├── pyproject.toml          # Configuración del proyecto y dependencias (uv)
├── uv.lock                 # Lockfile de dependencias
├── .env                    # Variables de entorno (local)
├── .env.example            # Ejemplo de variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── .python-version         # Versión de Python (3.14)
├── README.md               # Este archivo
├── MEMORIA.md              # Memoria técnica del proyecto
├── ARQUITECTURA_NEXUSGAMER.md  # Especificación técnica completa
├── DOCUMENTACION.md        # Plantilla base dfr-2026
├── requisitos.md           # Requisitos académicos del EFI
├── nexusgamer_schema.sql   # Esquema SQL completo (25 tablas, índices, triggers, seed)
├── src/
│   ├── manage.py           # Punto de entrada de Django
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── settings.py     # Configuración global
│   │   ├── urls.py         # URLs raíz y endpoints JWT / Swagger
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── usuarios/       # Perfil `persona` (1:1 con User de Django), direcciones (auth)
│   │   ├── catalogo/       # Categoria, Marca, Producto, Imagen, Especificacion, Variante
│   │   ├── carrito/        # Carrito persistente (user + session)
│   │   ├── ordenes/        # Órdenes, items, estados, historial
│   │   ├── pagos/          # Métodos de pago, pagos mock
│   │   ├── envios/         # Métodos de envío, zonas, cálculo
│   │   ├── promociones/    # Cupones, ofertas semanales
│   │   ├── wishlist/       # Lista de deseos
│   │   └── reviews/        # Reseñas y calificaciones
│   └── templates/
│       └── catalogo/
│           └── inicio.html # Vista principal de bienvenida
```

---

## 🗄️ Modelo de datos (Catálogo)

La app `catalogo` implementa 6 modelos con relaciones entre sí:

```
Categoria (1) ──┬──> Producto (N)
                │
Marca (1)  ─────┴──> Producto (N)
                │
Producto (1) ──┬──> ProductoImagen (N)
               ├──> Especificacion (N)
               └──> Variante (N)
```

| Modelo | Campos principales | Relaciones |
|--------|-------------------|------------|
| `Categoria` | nombre, slug, descripcion, imagen_url, categoria_padre (self-FK), orden, activa | Autoreferencial (jerarquía) |
| `Marca` | nombre, slug, logo_url, descripcion, pais_origen, activa | — |
| `Producto` | nombre, slug, sku, precio_lista, precio_oferta, stock_total, activo, destacado, fecha_lanzamiento | Marca (FK), Categoria (FK) |
| `ProductoImagen` | imagen_url, alt_text, orden, es_principal | Producto (FK) |
| `Especificacion` | nombre, valor, tipo, unidad, orden | Producto (FK) |
| `Variante` | sku_variante, nombre, precio_adicional, stock, atributos (JSON) | Producto (FK) |

> 📄 El esquema completo con las 25 tablas del proyecto (incluyendo usuarios, carrito, órdenes, pagos, envíos, promociones, wishlist, reviews) se encuentra en `nexusgamer_schema.sql`.

---

## 🔌 Endpoints API

Todos los endpoints están bajo el prefijo `/api/`.

### 🔐 Autenticación (`/api/`)

| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| POST | `/token/` | Obtener par de tokens JWT (access + refresh) | Público |
| POST | `/token/refresh/` | Renovar access token usando refresh token | Público |

### 📦 Catálogo (`/api/catalogo/`) — Público

| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | `/categorias/` | Listar categorías activas | Público |
| GET | `/categorias/{slug}/` | Detalle de categoría + productos paginados | Público |
| GET | `/marcas/` | Listar marcas activas | Público |
| GET | `/marcas/{slug}/` | Detalle de marca + productos | Público |
| GET | `/productos/` | Listar productos con filtros, búsqueda y paginación | Público |
| GET | `/productos/{slug}/` | Detalle completo de producto (anidado) | Público |
| GET | `/productos/destacados/` | Productos destacados (homepage) | Público |
| GET | `/productos/novedades/` | Últimos 20 lanzamientos | Público |
| GET | `/productos/ofertas/` | Productos con precio de oferta vigente | Público |
| GET | `/productos/buscar/?q=` | Búsqueda full-text por nombre, sku o descripción | Público |
| GET | `/imagenes/` | Listar imágenes de productos | Público |
| GET | `/especificaciones/` | Listar especificaciones de productos | Público |
| GET | `/variantes/` | Listar variantes de productos | Público |

### 💝 Wishlist (`/api/wishlist/`) — Autenticado

| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | `/items/` | Listar items de mi lista de deseos | Autenticado |
| POST | `/items/toggle/` | Agregar o quitar producto (toggle) | Autenticado |
| DELETE | `/items/{id}/` | Quitar item de la lista | Autenticado |
| DELETE | `/items/limpiar/` | Vaciar toda la lista de deseos | Autenticado |

### 🧭 Filtros disponibles en `/productos/`

```
?categoria__slug=gpus          # Filtrar por categoría
?marca__slug=nvidia            # Filtrar por marca
?precio_min=100000             # Precio mínimo
?precio_max=500000             # Precio máximo
?stock_disponible=true         # Solo productos con stock
?destacado=true                # Solo destacados
?ordenar=-precio_lista         # Ordenar por campo
?search=rtx                    # Búsqueda por nombre/sku/descripción
?por_pagina=24                 # Cantidad de resultados por página
```

### 📚 Documentación automática

| Endpoint | Descripción |
|----------|-------------|
| `/api/schema/` | Esquema OpenAPI 3 (JSON) |
| `/api/docs/` | Swagger UI interactiva |
| `/api/redoc/` | Redoc documentation |

### 🏠 Vista web

| Endpoint | Descripción |
|----------|-------------|
| `/catalogo/inicio/` | Vista principal con template de bienvenida |

---

## ✅ Requisitos académicos cumplidos

| # | Requisito | Estado | Evidencia |
|---|-----------|--------|-----------|
| 1 | ≥10 modelos en la BD | ✅ Planificado | 25 modelos en `nexusgamer_schema.sql` (6 implementados en catalogo) |
| 2 | Relaciones entre modelos | ✅ Completado | FKs, self-referencial (categoría padre) |
| 3 | Planificación BD en README | ✅ Completado | Ver sección "Modelo de datos" y `nexusgamer_schema.sql` |
| 4 | API REST habilitada | ✅ Completado | Django + DRF configurado y operativo |
| 5 | ≥8 modelos con ViewSet | ✅ Planificado | 6 ViewSets en catalogo + apps pendientes |
| 6 | ≥2 ViewSets con NestedSerializer | ✅ Completado | `ProductoPublicSerializer` anida marca, categoria, imágenes, specs, variantes |
| 7 | Auth Session + Token | ✅ Completado | JWT + SessionAuthentication en `settings.py` |
| 8 | ≥2 @action custom | ✅ Completado | `destacados`, `novedades`, `ofertas`, `buscar` |
| 9 | Paginación en get all | ✅ Completado | `PageNumberPagination` personalizado |
| 10 | ≥1 ViewSet con filtros/búsqueda | ✅ Completado | `ProductoViewSet` con django-filter + SearchFilter |
| 11 | Swagger / OpenAPI / Redoc | ✅ Completado | drf-spectacular en `/api/schema/`, `/api/docs/`, `/api/redoc/` |
| 12 | Vista principal con template | ✅ Completado | `catalogo/inicio/` con template HTML |
| 13 | Admin con filtros/búsqueda | ✅ Completado | `ModelAdmin` con `list_filter`, `search_fields`, `ordering` |
| 14 | uv como gestor | ✅ Completado | `pyproject.toml` + `uv.lock` |
| 15 | CORS configurado | ✅ Completado | `django-cors-headers` para `localhost:3000` |
| 16 | Dockerizado | ⏳ Pendiente | `Dockerfile` + `docker-compose.yml` |
| 17 | Git organizado | ⏳ Pendiente | Ramas, PRs, commits descriptivos |

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/nexusgamer-api.git
cd nexusgamer-api
```

### 2. Instalar dependencias con uv

```bash
# Sincronizar el entorno virtual
uv sync

# O instalar dependencias adicionales
uv add <paquete>
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta los valores:

```bash
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL, Redis, etc.
```

### 4. Configurar la base de datos

El proyecto usa **PostgreSQL**. Antes de ejecutar migraciones, crea la base de datos y ejecuta el esquema:

```bash
# Opción A: Ejecutar el esquema SQL completo (incluye seed data)
psql -U postgres -d nexusgamer -f nexusgamer_schema.sql

# Opción B: Crear solo las tablas de Django
uv run python src/manage.py migrate
```

> ⚠️ Nota: Las migraciones de Django y el esquema SQL de `nexusgamer_schema.sql` usan los mismos nombres de tabla (ej. `catalogo_categoria`, `persona`, `auth_user`). Se recomienda ejecutar uno u otro, no ambos, para evitar conflictos.

### 5. Ejecutar el servidor

```bash
uv run python src/manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

### 6. Probar los endpoints

```bash
# Listar productos
curl http://localhost:8000/api/catalogo/productos/

# Buscar productos
curl "http://localhost:8000/api/catalogo/productos/buscar/?q=rtx"

# Ver Swagger UI
open http://localhost:8000/api/docs/

# Vista principal
open http://localhost:8000/catalogo/inicio/
```

### 7. Ejecutar tests

```bash
uv run python src/manage.py test apps.catalogo
```

---

## ⚙️ Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Django
SECRET_KEY=tu-clave-secreta-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos PostgreSQL
DB_NAME=nexusgamer
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=prefer

# Redis (cache)
REDIS_URL=redis://127.0.0.1:6379/1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🗺️ Plan de trabajo por fases

```
┌──────────────────────────────────────────────────────────────┐
│ FASE 1  ✅ Setup inicial                                     │
│ FASE 2  ✅ Catálogo (app propia)                             │
│ FASE 3  ⏳ Auth + Usuario                                    │
│ FASE 4  ⏳ Carrito + Órdenes                                 │
│ FASE 5  ⏳ Pagos + Envíos (Mock)                             │
│ FASE 6  🔄 Promociones + Wishlist (✅) + Reviews                  │
│ FASE 7  ⏳ Performance + Observabilidad                      │
│ FASE 8  ⏳ Documentación + Deploy                            │
└──────────────────────────────────────────────────────────────┘
```

### Fase 1 — Setup inicial (Completada)

- `uv init` + dependencias
- Estructura `src/settings/` y `src/apps/`
- Perfil `persona` + migraciones
- drf-spectacular + Swagger UI
- CORS para `localhost:3000`
- Endpoints JWT

### Fase 2 — Catálogo (Completada — App propia)

- 6 modelos: Categoria, Marca, Producto, ProductoImagen, Especificacion, Variante
- Serializers duales (público anidado vs escritura plano)
- 6 ViewSets de solo lectura + 4 `@action`
- Filtros avanzados, búsqueda, paginación
- Admin completo
- Vista principal con template
- 17 tests automatizados

### Fase 6 — Wishlist (Completada)

- Modelos: `ListaDeseos` (1:1 con usuario), `ItemListaDeseos`
- ViewSet de items con `toggle`, `list`, `destroy`, `limpiar`
- Solo usuarios autenticados (propios items)
- Serializers con nested relations (producto, variante)


Ver `MEMORIA.md` para el detalle completo de cada fase.

---

## 👥 Equipo

| Integrante | App asignada | Rol | GitHub |
|------------|--------------|-----|--------|
| Integrante 1 | **Catalogo** | Backend API (esta app) | `@usuario1` |
| Integrante 2 | Auth + Usuario / Carrito + Órdenes | Backend API | `@usuario2` |
| Integrante 3 | Pagos + Envíos / Promociones + Wishlist + Reviews | Backend API | `@usuario3` |

> 💡 Cada integrante es responsable de su(s) app(s), integrando todo en el mismo proyecto Django bajo la rama `main`.

---

## 📸 Capturas del proyecto

> 🔧 Para completar la exposición, agregá capturas de pantalla aquí:

```
## 1. Swagger UI en funcionamiento
![Swagger UI](capturas/swagger.png)

## 2. Listado de productos en la API
![Productos API](capturas/productos-api.png)

## 3. Detalle de producto con relaciones anidadas
![Producto detalle](capturas/producto-detalle.png)

## 4. Panel de administración de Django
![Django Admin](capturas/admin.png)

## 5. Vista principal de bienvenida
![Vista inicio](capturas/inicio.png)

## 6. Tests pasando
![Tests](capturas/tests.png)
```

**Instrucciones:** Tomá capturas con tu navegador o Postman/Insomnia mostrando los endpoints funcionando y guardalas en la carpeta `capturas/`.


<div align="center">
  <p>Desarrollado con ❤️ para Ingeniería de Software — EFI</p>
  <p><b>NexusGamer</b> — Tu portal al gaming next-gen 🎮</p>
</div>
