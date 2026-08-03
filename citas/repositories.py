"""
Capa de ACCESO A DATOS (Repository) del módulo de citas.

Responsabilidad única: leer y escribir en la base de datos.
"""

from .models import Cita


class CitaRepository:

    def listar(self, estado=None, estilista=None, fecha=None):
        queryset = Cita.objects.select_related('servicio').all()

        if estado:
            queryset = queryset.filter(estado=estado)
        if estilista:
            queryset = queryset.filter(estilista=estilista)
        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset

    def obtener_por_id(self, cita_id):
        return Cita.objects.select_related('servicio').filter(pk=cita_id).first()

    def crear(self, datos):
        return Cita.objects.create(**datos)

    def actualizar(self, cita, datos):
        for campo, valor in datos.items():
            setattr(cita, campo, valor)
        cita.save()
        return cita

    def eliminar(self, cita):
        cita.delete()
