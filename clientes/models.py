from django.db import models


class Cliente(models.Model):
    """
    Módulo de Clientes de Stycheck (RF07).
    Representa el perfil de una persona que usa la plataforma para
    agendar citas: sus datos de contacto y si desea recibir
    notificaciones. Es independiente del login de Django: cualquier
    capa de aplicación (API o vistas web) puede reutilizarlo.
    """

    nombre_completo = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    acepta_notificaciones = models.BooleanField(
        default=True,
        help_text='Si desea recibir recordatorios de sus citas por correo/SMS.',
    )
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['nombre_completo']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombre_completo} ({self.email})'
