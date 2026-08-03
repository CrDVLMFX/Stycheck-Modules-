from django.db import models


class Estilista(models.Model):
    """
    Módulo de Estilistas de Stycheck (RF09 extendido).
    Reemplaza el listado fijo de estilistas que antes vivía como
    'choices' de texto dentro de Cita. Al ser un catálogo propio,
    se pueden agregar, editar o dar de baja estilistas sin tocar
    código, y cada una puede tener sus propias especialidades y
    días de trabajo.
    """

    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    nombre_completo = models.CharField(max_length=150)
    especialidad = models.CharField(
        max_length=100,
        help_text='Ej. Coloración, Cortes, Uñas, Maquillaje.',
    )
    dias_laborales = models.JSONField(
        default=list,
        help_text='Lista de días que trabaja, ej. ["lunes", "martes"].',
    )
    hora_inicio_jornada = models.TimeField(default='08:00')
    hora_fin_jornada = models.TimeField(default='18:00')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estilistas'
        ordering = ['nombre_completo']
        verbose_name = 'Estilista'
        verbose_name_plural = 'Estilistas'

    def __str__(self):
        return f'{self.nombre_completo} ({self.especialidad})'
