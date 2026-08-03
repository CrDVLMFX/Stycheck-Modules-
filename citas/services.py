"""
Capa de DOMINIO (Service) del módulo de citas (RF10, RF11).

Contiene toda la lógica de negocio: validar al cliente, verificar que
el servicio esté activo y aplicar la restricción del proyecto de
"mínimo 2 horas de anticipación". Esta clase es independiente de
Django REST Framework y de los formularios web: cualquiera de las dos
capas de aplicación (API o vistas HTML) puede reutilizarla.
"""

from datetime import datetime, timedelta

from django.utils import timezone

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .repositories import CitaRepository

ANTICIPACION_MINIMA_HORAS = 2


class CitaService:

    def __init__(self, repository=None):
        self.repository = repository or CitaRepository()

    # --- Casos de uso -----------------------------------------------

    def listar_citas(self, estado=None, estilista=None, fecha=None):
        return self.repository.listar(estado=estado, estilista=estilista, fecha=fecha)

    def obtener_cita(self, cita_id):
        cita = self.repository.obtener_por_id(cita_id)
        if not cita:
            raise NotFoundError(f'No existe una cita con id {cita_id}.')
        return cita

    def crear_cita(self, datos):
        self._validar_cliente(datos.get('nombre_cliente'))
        self._validar_servicio_activo(datos.get('servicio'))
        self._validar_anticipacion(datos.get('fecha'), datos.get('hora'))
        return self.repository.crear(datos)

    def actualizar_cita(self, cita_id, datos):
        cita = self.obtener_cita(cita_id)

        nombre_cliente = datos.get('nombre_cliente', cita.nombre_cliente)
        servicio = datos.get('servicio', cita.servicio)
        fecha = datos.get('fecha', cita.fecha)
        hora = datos.get('hora', cita.hora)

        self._validar_cliente(nombre_cliente)
        self._validar_servicio_activo(servicio)
        self._validar_anticipacion(fecha, hora)

        return self.repository.actualizar(cita, datos)

    def cancelar_cita(self, cita_id):
        """Cambia el estado a 'cancelada' sin eliminar el registro (RF11)."""
        cita = self.obtener_cita(cita_id)
        return self.repository.actualizar(cita, {'estado': 'cancelada'})

    def eliminar_cita(self, cita_id):
        cita = self.obtener_cita(cita_id)
        self.repository.eliminar(cita)

    # --- Reglas de negocio --------------------------------------------

    def _validar_cliente(self, nombre_cliente):
        if not nombre_cliente or len(nombre_cliente.strip()) < 3:
            raise ValidationDomainError(
                'El nombre del cliente debe tener al menos 3 caracteres.'
            )

    def _validar_servicio_activo(self, servicio):
        if servicio is None:
            raise ValidationDomainError('Debe seleccionar un servicio del catálogo.')
        if getattr(servicio, 'activo', True) is False:
            raise ValidationDomainError(
                'El servicio seleccionado no está activo actualmente.'
            )

    def _validar_anticipacion(self, fecha, hora):
        if not fecha or not hora:
            raise ValidationDomainError('La fecha y la hora son obligatorias.')

        fecha_hora_cita = datetime.combine(fecha, hora)
        # Hora local segun TIME_ZONE del proyecto (America/Bogota), no la
        # del servidor donde corra el proceso.
        ahora_local = timezone.localtime(timezone.now()).replace(tzinfo=None)
        limite_minimo = ahora_local + timedelta(hours=ANTICIPACION_MINIMA_HORAS)

        if fecha_hora_cita < limite_minimo:
            raise ValidationDomainError(
                f'El agendamiento solo puede realizarse con un mínimo de '
                f'{ANTICIPACION_MINIMA_HORAS} horas de anticipación.'
            )
