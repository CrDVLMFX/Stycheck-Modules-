"""
Serializers de Resena.

IMPORTANTE: aqui solo vive la validacion de FORMATO (tipos, campos
requeridos). Las reglas de NEGOCIO (cita atendida, resena unica,
etc.) viven en la capa de dominio: resenas/services.py.
"""

from rest_framework import serializers

from .models import Resena


class ResenaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cita.nombre_cliente', read_only=True)
    servicio_nombre = serializers.CharField(source='cita.servicio.nombre', read_only=True)
    estilista_display = serializers.CharField(
        source='cita.get_estilista_display', read_only=True
    )
    puntuacion_display = serializers.CharField(
        source='get_puntuacion_display', read_only=True
    )

    class Meta:
        model = Resena
        fields = [
            'id',
            'cita',
            'cliente_nombre',
            'servicio_nombre',
            'estilista_display',
            'puntuacion',
            'puntuacion_display',
            'comentario',
            'creado',
            'actualizado',
        ]
        read_only_fields = ['id', 'creado', 'actualizado']
