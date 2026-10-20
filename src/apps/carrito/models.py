from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Carrito(models.Model):
    """Carrito de compras (vinculado a usuario o sesión anónima)."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carritos',
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carrito_carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-actualizado_en']

    def __str__(self):
        return f'Carrito {self.pk} ({self.usuario or self.session_key})'


class CarritoItem(models.Model):
    """Ítem de un carrito de compras."""

    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name='items'
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.CASCADE,
        related_name='en_carritos',
    )
    variante = models.ForeignKey(
        'catalogo.Variante',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='en_carritos',
    )
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario_snapshot = models.DecimalField(max_digits=12, decimal_places=2)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carrito_item'
        verbose_name = 'Ítem de carrito'
        verbose_name_plural = 'Ítems de carrito'
        unique_together = [['carrito', 'producto', 'variante']]
        ordering = ['-agregado_en']

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre} en carrito {self.carrito_id}'

    @property
    def subtotal(self):
        return self.precio_unitario_snapshot * self.cantidad
