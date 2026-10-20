from django.contrib.auth.models import User
from django.db import models


class Persona(models.Model):
    """Perfil de usuario vinculado 1:1 al User por defecto de Django."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='persona',
    )
    dni = models.CharField(max_length=20, blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return self.user.username
