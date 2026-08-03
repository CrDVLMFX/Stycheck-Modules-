from django.contrib import admin

from .models import Resena


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = (
        'cita',
        'puntuacion',
        'creado',
    )
    list_filter = ('puntuacion',)
    search_fields = ('cita__nombre_cliente', 'comentario')
