from django.contrib import admin

from .models import Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'categoria',
        'duracion_minutos',
        'precio',
        'popular',
        'activo',
    )
    list_filter = ('categoria', 'popular', 'activo')
    search_fields = ('nombre', 'descripcion')
