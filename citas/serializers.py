"""
Serializers de Cita.

IMPORTANTE: aqui solo vive la validacion de FORMATO (tipos, campos
requeridos). Las reglas de NEGOCIO (anticipacion de 2h, servicio
activo, etc.) viven en la capa de dominio: citas/services.py.
"""

from rest_framework import serializers

from .models import Cita


class CitaSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    estilista_display = serializers.CharField(
        source='get_estilista_display', read_only=True
    )
    estado_display = serializers.CharField(
        source='get_estado_display', read_only=True
    )

    class Meta:
        model = Cita
        fields = [
            'id',
            'nombre_cliente',
            'servicio',
            'servicio_nombre',
            'estilista',
            'estilista_display',
            'fecha',
            'hora',
            'estado',
            'estado_display',
            'creado',
            'actualizado',
        ]
        read_only_fields = ['id', 'creado', 'actualizado']
