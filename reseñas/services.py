"""
Capa de DOMINIO (Service) del módulo de reseñas (RF12).

Contiene toda la lógica de negocio: solo se puede reseñar una cita
que ya fue "confirmada" (es decir, atendida) y cada cita admite una
única reseña. Esta clase es independiente de Django REST Framework y
de los formularios web: cualquiera de las dos capas de aplicación
(API o vistas HTML) puede reutilizarla.
"""

from stycheck.exceptions import NotFoundError, ValidationDomainError

from citas.repositories import CitaRepository

from .repositories import ResenaRepository

ESTADO_CITA_VALIDO_PARA_RESENA = 'confirmada'


class ResenaService:

    def __init__(self, repository=None, cita_repository=None):
        self.repository = repository or ResenaRepository()
        self.cita_repository = cita_repository or CitaRepository()

    # --- Casos de uso -----------------------------------------------

    def listar_resenas(self, puntuacion=None, estilista=None):
        return self.repository.listar(puntuacion=puntuacion, estilista=estilista)

    def obtener_resena(self, resena_id):
        resena = self.repository.obtener_por_id(resena_id)
        if not resena:
            raise NotFoundError(f'No existe una reseña con id {resena_id}.')
        return resena

    def crear_resena(self, datos):
        cita = self._validar_cita_existente(datos.get('cita'))
        self._validar_cita_atendida(cita)
        self._validar_resena_unica(cita)
        self._validar_puntuacion(datos.get('puntuacion'))
        return self.repository.crear(datos)

    def actualizar_resena(self, resena_id, datos):
        resena = self.obtener_resena(resena_id)

        puntuacion = datos.get('puntuacion', resena.puntuacion)
        self._validar_puntuacion(puntuacion)

        return self.repository.actualizar(resena, datos)

    def eliminar_resena(self, resena_id):
        resena = self.obtener_resena(resena_id)
        self.repository.eliminar(resena)

    # --- Reglas de negocio --------------------------------------------

    def _validar_cita_existente(self, cita):
        if cita is None:
            raise ValidationDomainError('Debe indicar la cita que desea reseñar.')
        return cita

    def _validar_cita_atendida(self, cita):
        if cita.estado != ESTADO_CITA_VALIDO_PARA_RESENA:
            raise ValidationDomainError(
                'Solo se pueden reseñar citas que ya fueron confirmadas y atendidas.'
            )

    def _validar_resena_unica(self, cita):
        if self.repository.obtener_por_cita(cita.id):
            raise ValidationDomainError('Esta cita ya cuenta con una reseña registrada.')

    def _validar_puntuacion(self, puntuacion):
        if puntuacion is None or not (1 <= int(puntuacion) <= 5):
            raise ValidationDomainError('La puntuación debe estar entre 1 y 5.')
