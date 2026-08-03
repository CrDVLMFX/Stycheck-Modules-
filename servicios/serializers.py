"""
Serializers de Servicio.

IMPORTANTE: aqui solo vive la validacion de FORMATO (tipos, campos
requeridos). Las reglas de NEGOCIO (precio > 0, nombre minimo, etc.)
viven en la capa de dominio: servicios/services.py.
"""

from rest_framework import serializers

from .models import Servicio


class ServicioSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(
        source='get_categoria_display', read_only=True
    )

    class Meta:
        model = Servicio
        fields = [
            'id',
            'nombre',
            'descripcion',
            'categoria',
            'categoria_display',
            'duracion_minutos',
            'precio',
            'popular',
            'activo',
            'creado',
            'actualizado',
        ]
        read_only_fields = ['id', 'creado', 'actualizado']
