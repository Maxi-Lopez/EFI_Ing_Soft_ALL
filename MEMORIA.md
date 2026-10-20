# MEMORIA DEL PROYECTO — NexusGamer API

## Estado actual

**Fecha:** 2026-10-18  
**Proyecto:** EFI Ingeniería de Software — Django REST Framework  
**Rama:** main (pendiente push a GitHub)  
**Estado:** Fase 1 y Fase 2 implementadas  

---

## Archivos existentes en `/home/maxi/Documents/ingenieriasoftware/djangorest/EFI_Ing_Software/`

| Archivo | Descripción |
|---------|-------------|
| `ARQUITECTURA_NEXUSGAMER.md` | Especificación técnica completa (25 modelos, 10 apps, endpoints, auth, deploy) |
| `DOCUMENTACION.md` | Plantilla base `dfr-2026` (estructura `src/settings/`, uv, JWT, convenciones) |
| `requisitos.md` | Requisitos académicos del EFI (≥10 modelos, ≥8 ViewSets, nested serializers, @action, paginación, filtros, Swagger, admin, uv, CORS, Docker, Git) |
| `nexusgamer_schema.sql` | Esquema SQL completo para PostgreSQL (620 líneas, 25 tablas, índices, triggers, seed data) |
| `README.md` | Documentación del proyecto para exposición (setup, arquitectura, endpoints, requisitos) |
| `pyproject.toml` + `uv.lock` | Gestor de paquetes `uv` con todas las dependencias |
| `.env` / `.env.example` | Variables de entorno (BD, Redis, CORS, Django) |
| `src/manage.py` | Punto de entrada de Django |
| `src/settings/` | Configuración Django (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`) |
| `src/apps/usuarios/` | Perfil `persona` (1:1 con User de Django) + admin + migración `0001_initial` |
| `src/apps/catalogo/` | 6 modelos, serializers duales, 6 ViewSets + 4 `@action`, admin, tests, template bienvenida |
| `src/apps/wishlist/` | Lista de deseos: `ListaDeseos` + `ItemListaDeseos`, ViewSet con `toggle`/`limpiar`, admin |
| `src/apps/{carrito,ordenes,pagos,envios,promociones,reviews}/` | Apps creadas (estructura vacía, pendiente implementar) |

---

## Decisiones técnicas tomadas

| Tema | Decisión |
|------|----------|
| **User por defecto + perfil `persona`** | `auth_user` de Django (`django.contrib.auth.models.User`) + tabla `persona` 1:1 con PK compartida (`user_id` = `auth_user.id`) (dni, telefono, fecha_nacimiento, avatar_url) |
| **BD** | PostgreSQL (Supabase ready) — SQL en `nexusgamer_schema.sql` |
| **PK** | `BIGSERIAL` / `BigAutoField` (compatibilidad Django) |
| **JSON/JSONB** | `JSONField` (atributos variante, promociones) |
| **Moneda** | `NUMERIC(12,2)` (`DecimalField`) |
| **Soft delete** | No — campo `activo`/`activa` boolean |
| **Carrito** | Dual: user XOR session_key (constraint CHECK) — planificado |
| **Órdenes** | Snapshot precios/stock en items; estados como lookup table — planificado |
| **Pagos/Envíos** | Mock educacional (sin credenciales reales) — planificado |
| **Auth** | JWT (SimpleJWT) + SessionAuthentication |
| **Documentación API** | drf-spectacular (OpenAPI 3) + Swagger UI + Redoc |
| **Cache** | Redis (Upstash) — configurado en settings |
| **Storage** | Supabase Storage (S3-compatible) — configurado en settings |
| **Gestor paquetes** | `uv` |
| **Estructura** | `src/` con paquete `settings/` y apps en `src/apps/` |

---

## Avance por fases

### Fase 1 — Setup inicial ✅ COMPLETADA

- [x] `uv init` + `uv add` dependencias (Django 6.1, DRF, SimpleJWT, django-filter, drf-spectacular, django-cors-headers, python-dotenv, psycopg2-binary, django-storages, boto3, redis, django-redis, gunicorn, django-environ)
- [x] Crear estructura `src/` con paquete `settings/`
- [x] Configurar perfil `persona` (1:1 con User de Django) + migraciones iniciales (`usuarios/migrations/0001_initial.py`)
- [x] Setup `drf-spectacular` + Swagger UI + Redoc (`/api/schema/`, `/api/docs/`, `/api/redoc/`)
- [x] Configurar CORS para `localhost:3000`
- [x] Endpoints JWT (`/api/token/`, `/api/token/refresh/`)
- [x] `manage.py check` → 0 issues

### Fase 2 — Catálogo (Core público) ✅ COMPLETADA

- [x] Models: Categoria, Marca, Producto, ProductoImagen, Especificacion, Variante (6 modelos)
- [x] Serializers con nested relations (público vs escritura)
- [x] ViewSets + `django-filter` avanzado
- [x] Paginación personalizada + ordering
- [x] 4 `@action` custom: `destacados`, `novedades`, `ofertas`, `buscar`
- [x] Admin completo con `list_filter`, `search_fields`, `ordering`, `prepopulated_fields`
- [x] Vista principal `inicio/` con template de bienvenida
- [x] Tests (17 tests: modelos + API)
- [x] Migraciones generadas (`catalogo/migrations/0001_initial.py`)

### Fase 3 — Auth + Usuario ⏳ PENDIENTE

- [ ] JWT endpoints personalizados (register, login, me, password change)
- [ ] Perfil + Direcciones CRUD
- [ ] Permisos `IsOwnerOrReadOnly`

### Fase 4 — Carrito + Órdenes ⏳ PENDIENTE

- [ ] Carrito persistente (user + session) + merge al login
- [ ] Checkout flow: carrito → orden (snapshot precios/stock)
- [ ] Validación stock atómico (`SELECT FOR UPDATE`)

### Fase 5 — Pagos + Envíos (Mock) ⏳ PENDIENTE

- [ ] Métodos de pago con cuotas
- [ ] Cálculo envío por zona/CP
- [ ] Webhook mock para testing

### Fase 6 — Promociones + Wishlist (✅) + Reviews 🔄 PARCIAL

- [ ] Cupón validation endpoint
- [ ] Ofertas semanales homepage
- [x] Wishlist toggle, list, destroy, limpiar (solo autenticados)
- [ ] Reviews solo verified purchase

### Fase 7 — Performance + Observabilidad ⏳ PENDIENTE

- [ ] Redis cache para listings
- [ ] Database indexes (GIN JSONB, trigram search)
- [ ] Logging estructurado + Sentry
- [ ] Rate limiting diferenciado

### Fase 8 — Documentación + Deploy ⏳ PENDIENTE

- [ ] OpenAPI spec completa (parcial: drf-spectacular configurado)
- [ ] Postman collection export
- [ ] README con setup local + deploy (Supabase + Vercel) — **este archivo**
- [ ] Dockerfile multi-stage
- [ ] GitHub repo con README + capturas

---

## Mapeo requisitos.md → Implementación

| Requisito | Estado | Comentario |
|-----------|--------|------------|
| ≥10 modelos | ✅ Planificado | 25 modelos en schema.sql (6 implementados en catalogo) |
| Relaciones entre modelos | ✅ Planificado | FKs, self-referencial (categoría padre) |
| Planificación BD en README | ✅ Completado | Incluido en `README.md` |
| API REST habilitada | ✅ Completado | Django + DRF configurado y funcionando |
| ≥8 modelos con ViewSet | ✅ Planificado | 6 ViewSets en catalogo + 4 apps pendientes |
| ≥2 ViewSets con NestedSerializer en list | ✅ Completado | Catalogo: Producto anida marca, categoria, imágenes, specs, variantes |
| Auth Session + Token | ✅ Completado | JWT + SessionAuthentication en settings |
| ≥2 @action custom | ✅ Completado | Catalogo: `destacados`, `novedades`, `ofertas`, `buscar` |
| Paginación en get all | ✅ Completado | DRF pagination class custom |
| ≥1 ViewSet con filtros/búsqueda | ✅ Completado | ProductoViewSet: filtros avanzados + search |
| OpenAPI/Swagger/Redoc | ✅ Completado | drf-spectacular configurado |
| Vista principal template | ✅ Completado | Vista `inicio/` con template HTML |
| Admin completo con filtros/búsqueda | ✅ Completado | ModelAdmin completo en catalogo |
| uv como gestor | ✅ Confirmado | pyproject.toml + uv.lock |
| CORS configurado | ✅ Completado | django-cors-headers para localhost:3000 |
| Dockerizado | ⏳ Pendiente | Dockerfile + docker-compose.yml |
| Git organizado (ramas, PRs, commits) | ⏳ Pendiente | Iniciar repo, conventional commits |

---

## Comandos útiles

```bash
# Ir al directorio
cd /home/maxi/Documents/ingenieriasoftware/djangorest/EFI_Ing_Software

# Activar entorno uv
source .venv/bin/activate  # o usar uv run

# Verificar que Django esté bien configurado
uv run python src/manage.py check

# Crear migraciones
uv run python src/manage.py makemigrations

# Aplicar migraciones (requiere PostgreSQL corriendo)
uv run python src/manage.py migrate

# Crear superusuario
uv run python src/manage.py createsuperuser

# Ejecutar servidor de desarrollo
uv run python src/manage.py runserver

# Ejecutar tests de catalogo
uv run python src/manage.py test apps.catalogo

# Acceder a la API
# Swagger UI: http://localhost:8000/api/docs/
# Redoc: http://localhost:8000/api/redoc/
# OpenAPI schema: http://localhost:8000/api/schema/
# API catálogo: http://localhost:8000/api/catalogo/
# Vista bienvenida: http://localhost:8000/catalogo/inicio/
```

---

## Notas para continuar

1. **PostgreSQL** — Ejecutar `nexusgamer_schema.sql` en dbgate/psql antes de correr `migrate` y tests.
2. **Arquitectura** — Seguir `ARQUITECTURA_NEXUSGAMER.md` como especificación maestra.
3. **Plantilla base** — `DOCUMENTACION.md` define la estructura `src/settings/` y convenciones.
4. **Requisitos académicos** — `requisitos.md` es la checklist de aprobación; mapeada arriba.
5. **Stack** — Python 3.14, Django 6.1, uv, PostgreSQL, JWT, Redis, S3.

---

## 👥 Equipo y roles

| Rol | Nombre | Responsabilidad |
|-----|--------|-----------------|
| Desarrollador | **Maxi** | App `catalogo` (modelos, serializers, ViewSets, admin, tests, template) |
| Mano derecha | **Keres** | Apoyo general, planificación, documentación, setup y coordinación |

---

**Última acción:** Implementadas Fase 1 (setup) y Fase 2 (app catalogo).  
**Siguiente acción:** Configurar PostgreSQL, ejecutar migraciones e implementar Fase 3 (Auth + Usuario).
