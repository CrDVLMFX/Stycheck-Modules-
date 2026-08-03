"""
Serializers de Cliente.

IMPORTANTE: aqui solo vive la validacion de FORMATO (tipos de dato,
campos requeridos, formato de email por Django). Las reglas de
NEGOCIO (telefono valido, email unico, etc.) viven en la capa de
dominio: clientes/services.py.
"""

from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre_completo',
            'email',
            'telefono',
            'acepta_notificaciones',
            'activo',
            'creado',
            'actualizado',
        ]
        read_only_fields = ['id', 'creado', 'actualizado']
