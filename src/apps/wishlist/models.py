from django.conf import settings
from django.db import models


class ListaDeseos(models.Model):
    """Lista de deseos de un usuario (1 por usuario)."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lista_deseos',
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wishlist_listadeseos'
        verbose_name = 'Lista de deseos'
        verbose_name_plural = 'Listas de deseos'

    def __str__(self):
        return f'Lista de {self.usuario.username}'


class ItemListaDeseos(models.Model):
    """Producto (y variante opcional) en la lista de deseos de un usuario."""

    lista = models.ForeignKey(
        ListaDeseos,
        on_delete=models.CASCADE,
        related_name='items',
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.CASCADE,
        related_name='en_listas_de_deseos',
    )
    variante = models.ForeignKey(
        'catalogo.Variante',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='en_listas_de_deseos',
    )
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlist_item'
        unique_together = [['lista', 'producto', 'variante']]
        verbose_name = 'Item de lista de deseos'
        verbose_name_plural = 'Items de lista de deseos'
        ordering = ['-agregado_en']

    def __str__(self):
        return f'{self.producto.nombre} ({self.lista.usuario.username})'
