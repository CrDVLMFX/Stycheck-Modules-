from django.contrib import admin

from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_cliente',
        'servicio',
        'estilista',
        'fecha',
        'hora',
        'estado',
    )
    list_filter = ('estado', 'estilista', 'fecha')
    search_fields = ('nombre_cliente', 'servicio__nombre')
