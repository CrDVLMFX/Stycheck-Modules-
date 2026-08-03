from django.db import models


class Servicio(models.Model):
    """
    Módulo de Catálogo de Servicios de Stycheck (RF09).
    Representa cada servicio ofrecido por el salón de belleza:
    nombre, descripción, categoría, duración estimada y precio.
    """

    CATEGORIA_CHOICES = [
        ('cabello', 'Cabello'),
        ('unas', 'Uñas'),
        ('facial', 'Facial'),
        ('spa', 'Spa'),
        ('maquillaje', 'Maquillaje'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=500)
    categoria = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default='cabello'
    )
    duracion_minutos = models.PositiveIntegerField(default=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    popular = models.BooleanField(
        default=False, help_text='Se mostrará en "Servicios populares" (RF08)'
    )
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'servicios'
        ordering = ['categoria', 'nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return f'{self.nombre} ({self.get_categoria_display()})'
