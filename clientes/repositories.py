"""
Capa de ACCESO A DATOS (Repository) del módulo de clientes.

Responsabilidad única: leer y escribir en la base de datos.
"""

from .models import Cliente


class ClienteRepository:

    def listar(self, activo=None, buscar=None):
        queryset = Cliente.objects.all()

        if activo is not None:
            queryset = queryset.filter(activo=activo)
        if buscar:
            queryset = queryset.filter(nombre_completo__icontains=buscar)

        return queryset

    def obtener_por_id(self, cliente_id):
        return Cliente.objects.filter(pk=cliente_id).first()

    def obtener_por_email(self, email):
        return Cliente.objects.filter(email__iexact=email).first()

    def crear(self, datos):
        return Cliente.objects.create(**datos)

    def actualizar(self, cliente, datos):
        for campo, valor in datos.items():
            setattr(cliente, campo, valor)
        cliente.save()
        return cliente

    def eliminar(self, cliente):
        cliente.delete()
