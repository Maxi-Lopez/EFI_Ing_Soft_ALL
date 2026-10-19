from django.db import models


class Categoria(models.Model):
    """Categoría de productos (jerárquica, autocontenida)."""

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True, null=True)
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias',
    )
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogo_categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def nivel(self):
        nivel = 0
        actual = self.categoria_padre
        while actual is not None:
            nivel += 1
            actual = actual.categoria_padre
        return nivel


class Marca(models.Model):
    """Marca de productos."""

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    descripcion = models.TextField(blank=True)
    pais_origen = models.CharField(max_length=100, blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogo_marca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto del catálogo gaming."""

    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion_corta = models.TextField(blank=True)
    descripcion_larga = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    precio_lista = models.DecimalField(max_digits=12, decimal_places=2)
    precio_oferta = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    iva_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=21.00
    )
    stock_total = models.PositiveIntegerField(default=0)
    stock_reservado = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_lanzamiento = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    marca = models.ForeignKey(
        Marca, on_delete=models.PROTECT, related_name='productos'
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos'
    )

    class Meta:
        db_table = 'catalogo_producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['marca', 'categoria']),
            models.Index(fields=['activo', 'destacado']),
            models.Index(fields=['precio_lista']),
        ]

    def __str__(self):
        return self.nombre

    @property
    def stock_disponible(self):
        return self.stock_total - self.stock_reservado


class ProductoImagen(models.Model):
    """Imágenes de un producto."""

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='imagenes'
    )
    imagen_url = models.URLField()
    alt_text = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    es_principal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalogo_productoimagen'
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de productos'
        ordering = ['orden', 'id']

    def __str__(self):
        return f'Imagen de {self.producto.nombre}'


class Especificacion(models.Model):
    """Especificación clave-valor de un producto."""

    TIPO_CHOICES = [
        ('text', 'Texto'),
        ('number', 'Número'),
        ('boolean', 'Booleano'),
    ]

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='especificaciones'
    )
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='text')
    unidad = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_especificacion'
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f'{self.nombre}: {self.valor}'


class Variante(models.Model):
    """Variante de un producto (color, talle, storage, etc.)."""

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='variantes'
    )
    sku_variante = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    precio_adicional = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    stock = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)
    atributos = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogo_variante'
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.producto.nombre} - {self.nombre}'
