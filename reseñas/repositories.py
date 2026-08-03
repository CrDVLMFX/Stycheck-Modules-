"""
Capa de ACCESO A DATOS (Repository) del módulo de reseñas.

Responsabilidad única: leer y escribir en la base de datos.
"""

from .models import Resena


class ResenaRepository:

    def listar(self, puntuacion=None, estilista=None):
        queryset = Resena.objects.select_related('cita', 'cita__servicio').all()

        if puntuacion:
            queryset = queryset.filter(puntuacion=puntuacion)
        if estilista:
            queryset = queryset.filter(cita__estilista=estilista)

        return queryset

    def obtener_por_id(self, resena_id):
        return Resena.objects.select_related('cita', 'cita__servicio').filter(pk=resena_id).first()

    def obtener_por_cita(self, cita_id):
        return Resena.objects.filter(cita_id=cita_id).first()

    def crear(self, datos):
        return Resena.objects.create(**datos)

    def actualizar(self, resena, datos):
        for campo, valor in datos.items():
            setattr(resena, campo, valor)
        resena.save()
        return resena

    def eliminar(self, resena):
        resena.delete()
