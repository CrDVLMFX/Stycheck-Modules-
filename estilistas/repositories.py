"""
Capa de ACCESO A DATOS (Repository) del módulo de estilistas.

Responsabilidad única: leer y escribir en la base de datos.
"""

from .models import Estilista


class EstilistaRepository:

    def listar(self, activo=None, especialidad=None, dia=None):
        queryset = Estilista.objects.all()

        if activo is not None:
            queryset = queryset.filter(activo=activo)
        if especialidad:
            queryset = queryset.filter(especialidad__icontains=especialidad)
        if dia:
            # Se filtra sobre la representacion de texto del JSON en vez
            # de "contains" nativo, ya que ese lookup solo esta soportado
            # en PostgreSQL/MySQL con JSON real y falla en SQLite (usado
            # en desarrollo). icontains funciona igual en ambos motores.
            queryset = queryset.filter(dias_laborales__icontains=dia)

        return queryset

    def obtener_por_id(self, estilista_id):
        return Estilista.objects.filter(pk=estilista_id).first()

    def crear(self, datos):
        return Estilista.objects.create(**datos)

    def actualizar(self, estilista, datos):
        for campo, valor in datos.items():
            setattr(estilista, campo, valor)
        estilista.save()
        return estilista

    def eliminar(self, estilista):
        estilista.delete()
