"""
Capa de DOMINIO (Service) del catálogo de servicios (RF08, RF09).

Aquí vive la lógica de negocio: qué hace válido o inválido a un
servicio. Esta clase no sabe qué es una request HTTP, un serializer
o un formulario: recibe datos simples (dict) y objetos de dominio, y
delega la persistencia al repositorio.
"""

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .repositories import ServicioRepository


class ServicioService:

    def __init__(self, repository=None):
        self.repository = repository or ServicioRepository()

    # --- Casos de uso -----------------------------------------------

    def listar_servicios(self, categoria=None, popular=None):
        return self.repository.listar(categoria=categoria, popular=popular)

    def obtener_servicio(self, servicio_id):
        servicio = self.repository.obtener_por_id(servicio_id)
        if not servicio:
            raise NotFoundError(f'No existe un servicio con id {servicio_id}.')
        return servicio

    def crear_servicio(self, datos):
        self._validar(datos)
        return self.repository.crear(datos)

    def actualizar_servicio(self, servicio_id, datos):
        servicio = self.obtener_servicio(servicio_id)

        datos_completos = {
            'nombre': datos.get('nombre', servicio.nombre),
            'precio': datos.get('precio', servicio.precio),
            'duracion_minutos': datos.get('duracion_minutos', servicio.duracion_minutos),
        }
        self._validar(datos_completos)

        return self.repository.actualizar(servicio, datos)

    def eliminar_servicio(self, servicio_id):
        servicio = self.obtener_servicio(servicio_id)
        self.repository.eliminar(servicio)

    # --- Reglas de negocio --------------------------------------------

    def _validar(self, datos):
        nombre = (datos.get('nombre') or '').strip()
        if len(nombre) < 3:
            raise ValidationDomainError(
                'El nombre del servicio debe tener al menos 3 caracteres.'
            )

        precio = datos.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationDomainError('El precio debe ser mayor a cero.')

        duracion = datos.get('duracion_minutos')
        if duracion is not None and duracion <= 0:
            raise ValidationDomainError(
                'La duración debe ser mayor a cero minutos.'
            )
