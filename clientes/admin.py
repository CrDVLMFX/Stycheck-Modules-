from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_completo',
        'email',
        'telefono',
        'activo',
    )
    list_filter = ('activo', 'acepta_notificaciones')
    search_fields = ('nombre_completo', 'email', 'telefono')
