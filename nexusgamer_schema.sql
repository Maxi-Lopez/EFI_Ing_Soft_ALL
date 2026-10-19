-- ============================================================
-- NEXUSGAMER - Esquema SQL para PostgreSQL
-- Basado en ARQUITECTURA_NEXUSGAMER.md
-- Listo para importar en dbgate
-- ============================================================

-- ============================================================
-- EXTENSIONES
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================================
-- 1. AUTH & USUARIOS
-- ============================================================

-- Tabla: users_usuario (Custom User Model)
CREATE TABLE users_usuario (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BOOLEAN DEFAULT FALSE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    date_joined TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    last_login TIMESTAMPTZ,
    dni VARCHAR(20),
    telefono VARCHAR(50),
    fecha_nacimiento DATE,
    avatar_url VARCHAR(500)
);

-- Índices para users_usuario
CREATE INDEX idx_users_usuario_email ON users_usuario(email);
CREATE INDEX idx_users_usuario_username ON users_usuario(username);
CREATE INDEX idx_users_usuario_is_active ON users_usuario(is_active);

-- Tabla: users_direccion
CREATE TABLE users_direccion (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES users_usuario(id) ON DELETE CASCADE,
    alias VARCHAR(100) NOT NULL,
    calle VARCHAR(200) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    piso VARCHAR(20),
    dpto VARCHAR(20),
    ciudad VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(20) NOT NULL,
    pais VARCHAR(2) DEFAULT 'AR' NOT NULL,
    es_predeterminada BOOLEAN DEFAULT FALSE NOT NULL,
    latitud NUMERIC(9, 6),
    longitud NUMERIC(9, 6)
);

-- Índices para users_direccion
CREATE INDEX idx_users_direccion_usuario_id ON users_direccion(usuario_id);
CREATE INDEX idx_users_direccion_es_predeterminada ON users_direccion(es_predeterminada);
CREATE INDEX idx_users_direccion_codigo_postal ON users_direccion(codigo_postal);

-- ============================================================
-- 2. CATALOGO
-- ============================================================

-- Tabla: catalogo_categoria
CREATE TABLE catalogo_categoria (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(500),
    categoria_padre_id BIGINT REFERENCES catalogo_categoria(id) ON DELETE SET NULL,
    orden INTEGER DEFAULT 0 NOT NULL,
    activa BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices para catalogo_categoria
CREATE INDEX idx_catalogo_categoria_slug ON catalogo_categoria(slug);
CREATE INDEX idx_catalogo_categoria_padre_id ON catalogo_categoria(categoria_padre_id);
CREATE INDEX idx_catalogo_categoria_activa ON catalogo_categoria(activa);
CREATE INDEX idx_catalogo_categoria_orden ON catalogo_categoria(orden);

-- Tabla: catalogo_marca
CREATE TABLE catalogo_marca (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    descripcion TEXT,
    pais_origen VARCHAR(100),
    activa BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices para catalogo_marca
CREATE INDEX idx_catalogo_marca_slug ON catalogo_marca(slug);
CREATE INDEX idx_catalogo_marca_activa ON catalogo_marca(activa);

-- Tabla: catalogo_producto
CREATE TABLE catalogo_producto (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    descripcion_corta VARCHAR(500),
    descripcion_larga TEXT,
    sku VARCHAR(100) UNIQUE NOT NULL,
    precio_lista NUMERIC(12, 2) NOT NULL CHECK (precio_lista >= 0),
    precio_oferta NUMERIC(12, 2) CHECK (precio_oferta >= 0),
    iva_porcentaje NUMERIC(5, 2) DEFAULT 21.00 NOT NULL CHECK (iva_porcentaje >= 0 AND iva_porcentaje <= 100),
    stock_total INTEGER DEFAULT 0 NOT NULL CHECK (stock_total >= 0),
    stock_reservado INTEGER DEFAULT 0 NOT NULL CHECK (stock_reservado >= 0),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    destacado BOOLEAN DEFAULT FALSE NOT NULL,
    fecha_lanzamiento DATE,
    marca_id BIGINT REFERENCES catalogo_marca(id) ON DELETE RESTRICT,
    categoria_id BIGINT REFERENCES catalogo_categoria(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para catalogo_producto
CREATE INDEX idx_catalogo_producto_slug ON catalogo_producto(slug);
CREATE INDEX idx_catalogo_producto_sku ON catalogo_producto(sku);
CREATE INDEX idx_catalogo_producto_marca_id ON catalogo_producto(marca_id);
CREATE INDEX idx_catalogo_producto_categoria_id ON catalogo_producto(categoria_id);
CREATE INDEX idx_catalogo_producto_activo ON catalogo_producto(activo);
CREATE INDEX idx_catalogo_producto_destacado ON catalogo_producto(destacado);
CREATE INDEX idx_catalogo_producto_fecha_lanzamiento ON catalogo_producto(fecha_lanzamiento);
CREATE INDEX idx_catalogo_producto_precio_lista ON catalogo_producto(precio_lista);
CREATE INDEX idx_catalogo_producto_nombre_trgm ON catalogo_producto USING GIN(nombre gin_trgm_ops);
CREATE INDEX idx_catalogo_producto_descripcion_trgm ON catalogo_producto USING GIN(descripcion_corta gin_trgm_ops);

-- Tabla: catalogo_productoimagen
CREATE TABLE catalogo_productoimagen (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    imagen_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    orden INTEGER DEFAULT 0 NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE NOT NULL
);

-- Índices para catalogo_productoimagen
CREATE INDEX idx_catalogo_productoimagen_producto_id ON catalogo_productoimagen(producto_id);
CREATE INDEX idx_catalogo_productoimagen_orden ON catalogo_productoimagen(orden);
CREATE INDEX idx_catalogo_productoimagen_es_principal ON catalogo_productoimagen(es_principal);

-- Tabla: catalogo_especificacion
CREATE TABLE catalogo_especificacion (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    valor VARCHAR(500) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'text' NOT NULL CHECK (tipo IN ('text', 'number', 'boolean')),
    unidad VARCHAR(50),
    orden INTEGER DEFAULT 0 NOT NULL
);

-- Índices para catalogo_especificacion
CREATE INDEX idx_catalogo_especificacion_producto_id ON catalogo_especificacion(producto_id);
CREATE INDEX idx_catalogo_especificacion_nombre ON catalogo_especificacion(nombre);
CREATE INDEX idx_catalogo_especificacion_orden ON catalogo_especificacion(orden);

-- Tabla: catalogo_variante
CREATE TABLE catalogo_variante (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    sku_variante VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    precio_adicional NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (precio_adicional >= 0),
    stock INTEGER DEFAULT 0 NOT NULL CHECK (stock >= 0),
    activa BOOLEAN DEFAULT TRUE NOT NULL,
    atributos JSONB
);

-- Índices para catalogo_variante
CREATE INDEX idx_catalogo_variante_producto_id ON catalogo_variante(producto_id);
CREATE INDEX idx_catalogo_variante_sku ON catalogo_variante(sku_variante);
CREATE INDEX idx_catalogo_variante_activa ON catalogo_variante(activa);
CREATE INDEX idx_catalogo_variante_atributos_gin ON catalogo_variante USING GIN(atributos);

-- ============================================================
-- 3. CARRITO
-- ============================================================

-- Tabla: carrito_carrito
CREATE TABLE carrito_carrito (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT REFERENCES users_usuario(id) ON DELETE CASCADE,
    session_key CHAR(40),
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    actualizado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CONSTRAINT carrito_user_or_session CHECK (
        (usuario_id IS NOT NULL AND session_key IS NULL) OR
        (usuario_id IS NULL AND session_key IS NOT NULL)
    )
);

-- Índices para carrito_carrito
CREATE UNIQUE INDEX idx_carrito_carrito_usuario_unique ON carrito_carrito(usuario_id) WHERE usuario_id IS NOT NULL;
CREATE INDEX idx_carrito_carrito_session_key ON carrito_carrito(session_key) WHERE session_key IS NOT NULL;
CREATE INDEX idx_carrito_carrito_actualizado ON carrito_carrito(actualizado_en);

-- Tabla: carrito_item
CREATE TABLE carrito_item (
    id BIGSERIAL PRIMARY KEY,
    carrito_id BIGINT NOT NULL REFERENCES carrito_carrito(id) ON DELETE CASCADE,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE RESTRICT,
    variante_id BIGINT REFERENCES catalogo_variante(id) ON DELETE SET NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario_snapshot NUMERIC(12, 2) NOT NULL CHECK (precio_unitario_snapshot >= 0),
    agregado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para carrito_item
CREATE INDEX idx_carrito_item_carrito_id ON carrito_item(carrito_id);
CREATE INDEX idx_carrito_item_producto_id ON carrito_item(producto_id);
CREATE INDEX idx_carrito_item_variante_id ON carrito_item(variante_id);
CREATE UNIQUE INDEX idx_carrito_item_carrito_producto_variante_unique ON carrito_item(carrito_id, producto_id, COALESCE(variante_id, -1));

-- ============================================================
-- 4. ORDENES
-- ============================================================

-- Tabla: ordenes_estadoorden
CREATE TABLE ordenes_estadoorden (
    id BIGSERIAL PRIMARY KEY,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    orden INTEGER DEFAULT 0 NOT NULL,
    color_hex VARCHAR(7)
);

-- Tabla: ordenes_orden
CREATE TABLE ordenes_orden (
    id BIGSERIAL PRIMARY KEY,
    numero_orden VARCHAR(50) UNIQUE NOT NULL,
    usuario_id BIGINT NOT NULL REFERENCES users_usuario(id) ON DELETE RESTRICT,
    estado_id BIGINT NOT NULL REFERENCES ordenes_estadoorden(id) ON DELETE RESTRICT DEFAULT 1,
    subtotal NUMERIC(12, 2) NOT NULL CHECK (subtotal >= 0),
    descuento_total NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (descuento_total >= 0),
    iva_total NUMERIC(12, 2) NOT NULL CHECK (iva_total >= 0),
    envio_total NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (envio_total >= 0),
    total_final NUMERIC(12, 2) NOT NULL CHECK (total_final >= 0),
    direccion_envio JSONB NOT NULL,
    metodo_envio_nombre VARCHAR(100),
    costo_envio NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (costo_envio >= 0),
    metodo_pago_nombre VARCHAR(100),
    cuotas INTEGER DEFAULT 1 CHECK (cuotas >= 1 AND cuotas <= 12),
    codigo_cupon VARCHAR(50),
    descuento_cupon NUMERIC(12, 2) DEFAULT 0.00 CHECK (descuento_cupon >= 0),
    notas_cliente TEXT,
    notas_internas TEXT,
    creada_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    confirmada_en TIMESTAMPTZ,
    enviada_en TIMESTAMPTZ,
    entregada_en TIMESTAMPTZ,
    cancelada_en TIMESTAMPTZ,
    cancelacion_motivo TEXT
);

-- Índices para ordenes_orden
CREATE INDEX idx_ordenes_orden_numero ON ordenes_orden(numero_orden);
CREATE INDEX idx_ordenes_orden_usuario_id ON ordenes_orden(usuario_id);
CREATE INDEX idx_ordenes_orden_estado_id ON ordenes_orden(estado_id);
CREATE INDEX idx_ordenes_orden_creada_en ON ordenes_orden(creada_en);
CREATE INDEX idx_ordenes_orden_total_final ON ordenes_orden(total_final);
CREATE INDEX idx_ordenes_orden_direccion_envio_gin ON ordenes_orden USING GIN(direccion_envio);

-- Tabla: ordenes_ordenitem
CREATE TABLE ordenes_ordenitem (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes_orden(id) ON DELETE CASCADE,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE RESTRICT,
    variante_id BIGINT REFERENCES catalogo_variante(id) ON DELETE SET NULL,
    nombre_snapshot VARCHAR(200) NOT NULL,
    sku_snapshot VARCHAR(100) NOT NULL,
    precio_unitario NUMERIC(12, 2) NOT NULL CHECK (precio_unitario >= 0),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    subtotal NUMERIC(12, 2) NOT NULL CHECK (subtotal >= 0),
    iva_porcentaje NUMERIC(5, 2) NOT NULL CHECK (iva_porcentaje >= 0 AND iva_porcentaje <= 100),
    iva_monto NUMERIC(12, 2) NOT NULL CHECK (iva_monto >= 0)
);

-- Índices para ordenes_ordenitem
CREATE INDEX idx_ordenes_ordenitem_orden_id ON ordenes_ordenitem(orden_id);
CREATE INDEX idx_ordenes_ordenitem_producto_id ON ordenes_ordenitem(producto_id);
CREATE INDEX idx_ordenes_ordenitem_variante_id ON ordenes_ordenitem(variante_id);

-- Tabla: ordenes_historialestado
CREATE TABLE ordenes_historialestado (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes_orden(id) ON DELETE CASCADE,
    estado_anterior_id BIGINT REFERENCES ordenes_estadoorden(id) ON DELETE SET NULL,
    estado_nuevo_id BIGINT NOT NULL REFERENCES ordenes_estadoorden(id) ON DELETE RESTRICT,
    usuario_id BIGINT REFERENCES users_usuario(id) ON DELETE SET NULL,
    notas TEXT,
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para ordenes_historialestado
CREATE INDEX idx_ordenes_historialestado_orden_id ON ordenes_historialestado(orden_id);
CREATE INDEX idx_ordenes_historialestado_creado_en ON ordenes_historialestado(creado_en);

-- ============================================================
-- 5. PROMOCIONES
-- ============================================================

-- Tabla: promociones_promocion
CREATE TABLE promociones_promocion (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('porcentaje', 'fijo', 'combo')),
    valor NUMERIC(12, 2) NOT NULL CHECK (valor >= 0),
    producto_ids JSONB,
    categoria_ids JSONB,
    marca_ids JSONB,
    requiere_cupon BOOLEAN DEFAULT FALSE NOT NULL,
    codigo_cupon VARCHAR(50) UNIQUE,
    fecha_inicio TIMESTAMPTZ NOT NULL,
    fecha_fin TIMESTAMPTZ,
    activa BOOLEAN DEFAULT TRUE NOT NULL,
    max_usos_global INTEGER CHECK (max_usos_global >= 0),
    max_usos_usuario INTEGER DEFAULT 1 CHECK (max_usos_usuario >= 0),
    usos_actuales INTEGER DEFAULT 0 NOT NULL CHECK (usos_actuales >= 0),
    aplica_envio_gratis BOOLEAN DEFAULT FALSE NOT NULL,
    minimo_compra NUMERIC(12, 2) DEFAULT 0.00 CHECK (minimo_compra >= 0)
);

-- Índices para promociones_promocion
CREATE INDEX idx_promociones_promocion_slug ON promociones_promocion(slug);
CREATE INDEX idx_promociones_promocion_codigo_cupon ON promociones_promocion(codigo_cupon) WHERE codigo_cupon IS NOT NULL;
CREATE INDEX idx_promociones_promocion_activa ON promociones_promocion(activa);
CREATE INDEX idx_promociones_promocion_fechas ON promociones_promocion(fecha_inicio, fecha_fin);
CREATE INDEX idx_promociones_promocion_tipo ON promociones_promocion(tipo);
CREATE INDEX idx_promociones_promocion_producto_ids_gin ON promociones_promocion USING GIN(producto_ids);
CREATE INDEX idx_promociones_promocion_categoria_ids_gin ON promociones_promocion USING GIN(categoria_ids);
CREATE INDEX idx_promociones_promocion_marca_ids_gin ON promociones_promocion USING GIN(marca_ids);

-- Tabla: promociones_ofertasemanal
CREATE TABLE promociones_ofertasemanal (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    precio_oferta NUMERIC(12, 2) NOT NULL CHECK (precio_oferta >= 0),
    fecha_inicio TIMESTAMPTZ NOT NULL,
    fecha_fin TIMESTAMPTZ,
    posicion_homepage INTEGER DEFAULT 0 NOT NULL,
    activa BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices para promociones_ofertasemanal
CREATE INDEX idx_promociones_ofertasemanal_producto_id ON promociones_ofertasemanal(producto_id);
CREATE INDEX idx_promociones_ofertasemanal_fechas ON promociones_ofertasemanal(fecha_inicio, fecha_fin);
CREATE INDEX idx_promociones_ofertasemanal_activa ON promociones_ofertasemanal(activa);
CREATE INDEX idx_promociones_ofertasemanal_posicion ON promociones_ofertasemanal(posicion_homepage);

-- ============================================================
-- 6. PAGOS (MOCK)
-- ============================================================

-- Tabla: pagos_metodopago
CREATE TABLE pagos_metodopago (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    tiene_cuotas BOOLEAN DEFAULT TRUE NOT NULL,
    max_cuotas INTEGER DEFAULT 12 CHECK (max_cuotas >= 1 AND max_cuotas <= 12),
    interes_cuotas JSONB
);

-- Índices para pagos_metodopago
CREATE INDEX idx_pagos_metodopago_codigo ON pagos_metodopago(codigo);
CREATE INDEX idx_pagos_metodopago_activo ON pagos_metodopago(activo);

-- Tabla: pagos_pago
CREATE TABLE pagos_pago (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT UNIQUE NOT NULL REFERENCES ordenes_orden(id) ON DELETE CASCADE,
    metodo_pago_id BIGINT NOT NULL REFERENCES pagos_metodopago(id) ON DELETE RESTRICT,
    monto NUMERIC(12, 2) NOT NULL CHECK (monto >= 0),
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('pendiente', 'aprobado', 'rechazado', 'reembolsado')),
    cuotas INTEGER DEFAULT 1 CHECK (cuotas >= 1 AND cuotas <= 12),
    external_id VARCHAR(100),
    payload_respuesta JSONB,
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    aprobado_en TIMESTAMPTZ
);

-- Índices para pagos_pago
CREATE INDEX idx_pagos_pago_orden_id ON pagos_pago(orden_id);
CREATE INDEX idx_pagos_pago_metodo_pago_id ON pagos_pago(metodo_pago_id);
CREATE INDEX idx_pagos_pago_estado ON pagos_pago(estado);
CREATE INDEX idx_pagos_pago_creado_en ON pagos_pago(creado_en);
CREATE INDEX idx_pagos_pago_external_id ON pagos_pago(external_id) WHERE external_id IS NOT NULL;
CREATE INDEX idx_pagos_pago_payload_gin ON pagos_pago USING GIN(payload_respuesta);

-- ============================================================
-- 7. ENVIOS
-- ============================================================

-- Tabla: envios_metodoenvio
CREATE TABLE envios_metodoenvio (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    costo_base NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (costo_base >= 0),
    costo_por_km NUMERIC(10, 2) DEFAULT 0.00 CHECK (costo_por_km >= 0),
    gratis_desde_monto NUMERIC(12, 2) DEFAULT 0.00 CHECK (gratis_desde_monto >= 0),
    tiempo_estimado_min_dias INTEGER DEFAULT 1 CHECK (tiempo_estimado_min_dias >= 0),
    tiempo_estimado_max_dias INTEGER DEFAULT 3 CHECK (tiempo_estimado_max_dias >= tiempo_estimado_min_dias),
    activo BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices para envios_metodoenvio
CREATE INDEX idx_envios_metodoenvio_codigo ON envios_metodoenvio(codigo);
CREATE INDEX idx_envios_metodoenvio_activo ON envios_metodoenvio(activo);

-- Tabla: envios_zonaenvio
CREATE TABLE envios_zonaenvio (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    codigo_postal_desde VARCHAR(20) NOT NULL,
    codigo_postal_hasta VARCHAR(20) NOT NULL,
    factor_costo NUMERIC(5, 3) DEFAULT 1.000 NOT NULL CHECK (factor_costo >= 0),
    activo BOOLEAN DEFAULT TRUE NOT NULL
);

-- Índices para envios_zonaenvio
CREATE INDEX idx_envios_zonaenvio_provincia ON envios_zonaenvio(provincia);
CREATE INDEX idx_envios_zonaenvio_cp_desde ON envios_zonaenvio(codigo_postal_desde);
CREATE INDEX idx_envios_zonaenvio_cp_hasta ON envios_zonaenvio(codigo_postal_hasta);
CREATE INDEX idx_envios_zonaenvio_activo ON envios_zonaenvio(activo);

-- Tabla: envios_envio
CREATE TABLE envios_envio (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT UNIQUE NOT NULL REFERENCES ordenes_orden(id) ON DELETE CASCADE,
    metodo_envio_id BIGINT NOT NULL REFERENCES envios_metodoenvio(id) ON DELETE RESTRICT,
    zona_id BIGINT REFERENCES envios_zonaenvio(id) ON DELETE SET NULL,
    costo_calculado NUMERIC(12, 2) NOT NULL CHECK (costo_calculado >= 0),
    tracking_number VARCHAR(100),
    transportadora VARCHAR(100),
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('pendiente', 'despachado', 'en_transito', 'entregado', 'devuelto')),
    despachado_en TIMESTAMPTZ,
    entregado_en TIMESTAMPTZ,
    payload_tracking JSONB
);

-- Índices para envios_envio
CREATE INDEX idx_envios_envio_orden_id ON envios_envio(orden_id);
CREATE INDEX idx_envios_envio_metodo_envio_id ON envios_envio(metodo_envio_id);
CREATE INDEX idx_envios_envio_zona_id ON envios_envio(zona_id);
CREATE INDEX idx_envios_envio_estado ON envios_envio(estado);
CREATE INDEX idx_envios_envio_tracking ON envios_envio(tracking_number) WHERE tracking_number IS NOT NULL;
CREATE INDEX idx_envios_envio_payload_gin ON envios_envio USING GIN(payload_tracking);

-- ============================================================
-- 8. WISHLIST & REVIEWS
-- ============================================================

-- Tabla: wishlist_listadeseos
CREATE TABLE wishlist_listadeseos (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT UNIQUE NOT NULL REFERENCES users_usuario(id) ON DELETE CASCADE,
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    actualizado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para wishlist_listadeseos
CREATE UNIQUE INDEX idx_wishlist_listadeseos_usuario_id ON wishlist_listadeseos(usuario_id);

-- Tabla: wishlist_item
CREATE TABLE wishlist_item (
    id BIGSERIAL PRIMARY KEY,
    lista_id BIGINT NOT NULL REFERENCES wishlist_listadeseos(id) ON DELETE CASCADE,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    variante_id BIGINT REFERENCES catalogo_variante(id) ON DELETE SET NULL,
    agregado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para wishlist_item
CREATE INDEX idx_wishlist_item_lista_id ON wishlist_item(lista_id);
CREATE INDEX idx_wishlist_item_producto_id ON wishlist_item(producto_id);
CREATE INDEX idx_wishlist_item_variante_id ON wishlist_item(variante_id);
CREATE UNIQUE INDEX idx_wishlist_item_lista_producto_variante_unique ON wishlist_item(lista_id, producto_id, COALESCE(variante_id, -1));

-- Tabla: reviews_resena
CREATE TABLE reviews_resena (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    usuario_id BIGINT NOT NULL REFERENCES users_usuario(id) ON DELETE CASCADE,
    orden_item_id BIGINT REFERENCES ordenes_ordenitem(id) ON DELETE SET NULL,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 1 AND puntuacion <= 5),
    titulo VARCHAR(200),
    comentario TEXT NOT NULL,
    verificada BOOLEAN DEFAULT FALSE NOT NULL,
    util_count INTEGER DEFAULT 0 NOT NULL CHECK (util_count >= 0),
    creada_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    actualizada_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Índices para reviews_resena
CREATE INDEX idx_reviews_resena_producto_id ON reviews_resena(producto_id);
CREATE INDEX idx_reviews_resena_usuario_id ON reviews_resena(usuario_id);
CREATE INDEX idx_reviews_resena_orden_item_id ON reviews_resena(orden_item_id);
CREATE INDEX idx_reviews_resena_puntuacion ON reviews_resena(puntuacion);
CREATE INDEX idx_reviews_resena_verificada ON reviews_resena(verificada);
CREATE INDEX idx_reviews_resena_creada_en ON reviews_resena(creada_en);
CREATE UNIQUE INDEX idx_reviews_resena_usuario_producto_unique ON reviews_resena(usuario_id, producto_id) WHERE orden_item_id IS NULL;
CREATE UNIQUE INDEX idx_reviews_resena_orden_item_unique ON reviews_resena(orden_item_id) WHERE orden_item_id IS NOT NULL;

-- Tabla: reviews_resenaimagen
CREATE TABLE reviews_resenaimagen (
    id BIGSERIAL PRIMARY KEY,
    resena_id BIGINT NOT NULL REFERENCES reviews_resena(id) ON DELETE CASCADE,
    imagen_url VARCHAR(500) NOT NULL,
    orden INTEGER DEFAULT 0 NOT NULL
);

-- Índices para reviews_resenaimagen
CREATE INDEX idx_reviews_resenaimagen_resena_id ON reviews_resenaimagen(resena_id);
CREATE INDEX idx_reviews_resenaimagen_orden ON reviews_resenaimagen(orden);

-- ============================================================
-- TRIGGERS PARA updated_at
-- ============================================================

-- Función genérica para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para catalogo_producto
CREATE TRIGGER tr_catalogo_producto_updated_at
    BEFORE UPDATE ON catalogo_producto
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para carrito_carrito
CREATE TRIGGER tr_carrito_carrito_updated_at
    BEFORE UPDATE ON carrito_carrito
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para wishlist_listadeseos
CREATE TRIGGER tr_wishlist_listadeseos_updated_at
    BEFORE UPDATE ON wishlist_listadeseos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para reviews_resena
CREATE TRIGGER tr_reviews_resena_updated_at
    BEFORE UPDATE ON reviews_resena
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- DATOS SEMILLA MINIMOS
-- ============================================================

-- Estados de orden
INSERT INTO ordenes_estadoorden (codigo, nombre, descripcion, orden, color_hex) VALUES
('pendiente', 'Pendiente', 'Orden creada, pendiente de confirmación', 1, '#FFA500'),
('confirmado', 'Confirmado', 'Orden confirmada, pendiente de preparación', 2, '#1E90FF'),
('preparando', 'Preparando', 'Orden en preparación', 3, '#9370DB'),
('enviado', 'Enviado', 'Orden enviada', 4, '#00CED1'),
('entregado', 'Entregado', 'Orden entregada', 5, '#228B22'),
('cancelado', 'Cancelado', 'Orden cancelada', 6, '#DC143C')
ON CONFLICT (codigo) DO NOTHING;

-- Métodos de pago
INSERT INTO pagos_metodopago (nombre, codigo, descripcion, activo, tiene_cuotas, max_cuotas, interes_cuotas) VALUES
('MercadoPago - Crédito', 'mp_credito', 'Pago con tarjeta de crédito vía MercadoPago', TRUE, TRUE, 12, '{"3": 0, "6": 0, "12": 15}'),
('MercadoPago - Débito', 'mp_debito', 'Pago con tarjeta de débito vía MercadoPago', TRUE, FALSE, 1, '{"1": 0}'),
('MercadoPago - Efectivo', 'mp_efectivo', 'Pago en efectivo vía MercadoPago', TRUE, FALSE, 1, '{"1": 0}'),
('Transferencia Bancaria', 'transferencia', 'Transferencia o depósito bancario', TRUE, FALSE, 1, '{"1": 0}')
ON CONFLICT (codigo) DO NOTHING;

-- Métodos de envío
INSERT INTO envios_metodoenvio (nombre, codigo, descripcion, costo_base, costo_por_km, gratis_desde_monto, tiempo_estimado_min_dias, tiempo_estimado_max_dias, activo) VALUES
('Envío Estándar', 'estandar', 'Envío a domicilio estándar', 2500.00, 50.00, 50000.00, 3, 7, TRUE),
('Envío Express', 'express', 'Envío a domicilio express', 4500.00, 80.00, 100000.00, 1, 2, TRUE),
('Retiro en Sucursal', 'retiro', 'Retiro en sucursal sin costo', 0.00, 0.00, 0.00, 0, 0, TRUE)
ON CONFLICT (codigo) DO NOTHING;

-- Categorías raíz ejemplo
INSERT INTO catalogo_categoria (nombre, slug, descripcion, orden, activa) VALUES
('Hardware', 'hardware', 'Componentes de PC', 1, TRUE),
('Periféricos', 'perifericos', 'Periféricos y accesorios', 2, TRUE),
('Consolas', 'consolas', 'Consolas de videojuegos', 3, TRUE),
('Monitores', 'monitores', 'Monitores y displays', 4, TRUE),
('Sillas Gaming', 'sillas-gaming', 'Sillas ergonómicas para gaming', 5, TRUE)
ON CONFLICT (slug) DO NOTHING;

-- Marcas ejemplo
INSERT INTO catalogo_marca (nombre, slug, descripcion, pais_origen, activa) VALUES
('NVIDIA', 'nvidia', 'Tarjetas gráficas NVIDIA', 'USA', TRUE),
('AMD', 'amd', 'Procesadores y GPUs AMD', 'USA', TRUE),
('ASUS', 'asus', 'Hardware gaming', 'Taiwan', TRUE),
('MSI', 'msi', 'Hardware gaming', 'Taiwan', TRUE),
('Logitech', 'logitech', 'Periféricos gaming', 'Suiza', TRUE),
('Razer', 'razer', 'Periféricos gaming', 'USA', TRUE)
ON CONFLICT (slug) DO NOTHING;

-- ============================================================
-- FIN DEL ESQUEMA
-- ============================================================