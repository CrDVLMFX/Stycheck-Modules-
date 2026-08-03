"""
Capa de ACCESO A DATOS (Repository) del catálogo de servicios.

Responsabilidad única: leer y escribir en la base de datos. No valida
reglas de negocio, no sabe nada de HTTP. Si mañana cambiamos el motor
de base de datos o pasamos a otra fuente de datos, este es el único
archivo que debería cambiar.
"""

from .models import Servicio


class ServicioRepository:

    def listar(self, categoria=None, popular=None):
        queryset = Servicio.objects.all().order_by('categoria', 'nombre')

        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if popular is not None:
            queryset = queryset.filter(popular=popular)

        return queryset

    def obtener_por_id(self, servicio_id):
        return Servicio.objects.filter(pk=servicio_id).first()

    def crear(self, datos):
        return Servicio.objects.create(**datos)

    def actualizar(self, servicio, datos):
        for campo, valor in datos.items():
            setattr(servicio, campo, valor)
        servicio.save()
        return servicio

    def eliminar(self, servicio):
        servicio.delete()
