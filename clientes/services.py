"""
Capa de DOMINIO (Service) del módulo de clientes (RF07).

Contiene la lógica de negocio: validar formato básico de datos de
contacto y evitar correos duplicados. Esta clase es independiente de
Django REST Framework y de los formularios web.
"""

import re

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .repositories import ClienteRepository

PATRON_TELEFONO = re.compile(r'^\+?\d{7,15}$')


class ClienteService:

    def __init__(self, repository=None):
        self.repository = repository or ClienteRepository()

    # --- Casos de uso -----------------------------------------------

    def listar_clientes(self, activo=None, buscar=None):
        return self.repository.listar(activo=activo, buscar=buscar)

    def obtener_cliente(self, cliente_id):
        cliente = self.repository.obtener_por_id(cliente_id)
        if not cliente:
            raise NotFoundError(f'No existe un cliente con id {cliente_id}.')
        return cliente

    def crear_cliente(self, datos):
        self._validar_nombre(datos.get('nombre_completo'))
        self._validar_telefono(datos.get('telefono'))
        self._validar_email_unico(datos.get('email'))
        return self.repository.crear(datos)

    def actualizar_cliente(self, cliente_id, datos):
        cliente = self.obtener_cliente(cliente_id)

        nombre = datos.get('nombre_completo', cliente.nombre_completo)
        telefono = datos.get('telefono', cliente.telefono)
        email = datos.get('email', cliente.email)

        self._validar_nombre(nombre)
        self._validar_telefono(telefono)
        if email != cliente.email:
            self._validar_email_unico(email)

        return self.repository.actualizar(cliente, datos)

    def desactivar_cliente(self, cliente_id):
        """Da de baja lógica al cliente sin eliminar su historial (RF07)."""
        cliente = self.obtener_cliente(cliente_id)
        return self.repository.actualizar(cliente, {'activo': False})

    def eliminar_cliente(self, cliente_id):
        cliente = self.obtener_cliente(cliente_id)
        self.repository.eliminar(cliente)

    # --- Reglas de negocio --------------------------------------------

    def _validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValidationDomainError(
                'El nombre completo debe tener al menos 3 caracteres.'
            )

    def _validar_telefono(self, telefono):
        if not telefono or not PATRON_TELEFONO.match(telefono.strip()):
            raise ValidationDomainError(
                'El teléfono debe contener entre 7 y 15 dígitos, con "+" opcional al inicio.'
            )

    def _validar_email_unico(self, email):
        if not email:
            raise ValidationDomainError('El correo electrónico es obligatorio.')
        if self.repository.obtener_por_email(email):
            raise ValidationDomainError('Ya existe un cliente registrado con ese correo.')
