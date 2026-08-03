from django.db import models

from servicios.models import Servicio


class Cita(models.Model):
    """
    Módulo de Agendamiento y Gestión de Citas de Stycheck (RF10, RF11).
    Permite al cliente seleccionar un servicio, fecha, hora y estilista
    para reservar una cita, y consultarla/cancelarla desde su perfil.
    """

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    ESTILISTA_CHOICES = [
        ('maria_gonzalez', 'María González'),
        ('valentina_torres', 'Valentina Torres'),
        ('laura_ramirez', 'Laura Ramírez'),
    ]

    nombre_cliente = models.CharField(max_length=150)
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name='citas',
        help_text='Servicio del catálogo seleccionado para esta cita (RF09).',
    )
    estilista = models.CharField(max_length=30, choices=ESTILISTA_CHOICES)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='pendiente'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'citas'
        ordering = ['fecha', 'hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        servicio_nombre = getattr(self.servicio, 'nombre', '')
        return (
            f'{self.nombre_cliente} · {servicio_nombre} '
            f'({self.fecha} {self.hora})'
        )
