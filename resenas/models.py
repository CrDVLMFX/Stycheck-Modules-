from django.db import models

from citas.models import Cita


class Resena(models.Model):
    """
    Módulo de Reseñas y Calificaciones de Stycheck (RF12).
    Permite al cliente calificar el servicio recibido una vez su cita
    haya sido atendida, dejando una puntuación (1 a 5 estrellas) y un
    comentario opcional. Cada cita solo puede tener una reseña.
    """

    PUNTUACION_CHOICES = [
        (1, '1 - Muy insatisfecho'),
        (2, '2 - Insatisfecho'),
        (3, '3 - Neutral'),
        (4, '4 - Satisfecho'),
        (5, '5 - Muy satisfecho'),
    ]

    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name='resena',
        help_text='Cita sobre la que se deja la reseña (RF12).',
    )
    puntuacion = models.PositiveSmallIntegerField(choices=PUNTUACION_CHOICES)
    comentario = models.TextField(max_length=500, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resenas'
        ordering = ['-creado']
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'

    def __str__(self):
        return f'{self.cita.nombre_cliente} · {self.puntuacion} estrellas'
