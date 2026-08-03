from django.contrib import admin

from .models import Estilista


@admin.register(Estilista)
class EstilistaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_completo',
        'especialidad',
        'hora_inicio_jornada',
        'hora_fin_jornada',
        'activo',
    )
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre_completo', 'especialidad')
