"""
Serializers de Estilista.

IMPORTANTE: aqui solo vive la validacion de FORMATO. Las reglas de
NEGOCIO (dias validos, horario coherente, disponibilidad) viven en
la capa de dominio: estilistas/services.py.
"""

from rest_framework import serializers

from .models import Estilista


class EstilistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estilista
        fields = [
            'id',
            'nombre_completo',
            'especialidad',
            'dias_laborales',
            'hora_inicio_jornada',
            'hora_fin_jornada',
            'activo',
            'creado',
            'actualizado',
        ]
        read_only_fields = ['id', 'creado', 'actualizado']
