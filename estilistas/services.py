"""
Capa de DOMINIO (Service) del módulo de estilistas.

Contiene la lógica de negocio: validar datos básicos y la regla de
disponibilidad (día laboral + horario de jornada). Esta clase es
independiente de Django REST Framework.

Nota de diseño: por decisión del equipo, el módulo de Citas sigue
usando su propio campo de texto (ESTILISTA_CHOICES) para no romper
la API ya entregada. Este catálogo de Estilistas queda desacoplado
e informativo por ahora; 'validar_disponibilidad' está lista para
conectarse desde CitaService el día que se decida migrar el campo
'estilista' de Cita a una ForeignKey hacia este módulo.
"""

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .repositories import EstilistaRepository

DIAS_SEMANA_ES = [
    'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo',
]


class EstilistaService:

    def __init__(self, repository=None):
        self.repository = repository or EstilistaRepository()

    # --- Casos de uso -----------------------------------------------

    def listar_estilistas(self, activo=None, especialidad=None, dia=None):
        return self.repository.listar(activo=activo, especialidad=especialidad, dia=dia)

    def obtener_estilista(self, estilista_id):
        estilista = self.repository.obtener_por_id(estilista_id)
        if not estilista:
            raise NotFoundError(f'No existe una estilista con id {estilista_id}.')
        return estilista

    def crear_estilista(self, datos):
        self._validar_nombre(datos.get('nombre_completo'))
        self._validar_dias(datos.get('dias_laborales', []))
        self._validar_horario(datos.get('hora_inicio_jornada'), datos.get('hora_fin_jornada'))
        return self.repository.crear(datos)

    def actualizar_estilista(self, estilista_id, datos):
        estilista = self.obtener_estilista(estilista_id)

        nombre = datos.get('nombre_completo', estilista.nombre_completo)
        dias = datos.get('dias_laborales', estilista.dias_laborales)
        inicio = datos.get('hora_inicio_jornada', estilista.hora_inicio_jornada)
        fin = datos.get('hora_fin_jornada', estilista.hora_fin_jornada)

        self._validar_nombre(nombre)
        self._validar_dias(dias)
        self._validar_horario(inicio, fin)

        return self.repository.actualizar(estilista, datos)

    def desactivar_estilista(self, estilista_id):
        """Baja lógica: ya no se le pueden asignar citas nuevas, pero
        conserva su historial (citas y reseñas pasadas)."""
        estilista = self.obtener_estilista(estilista_id)
        return self.repository.actualizar(estilista, {'activo': False})

    def eliminar_estilista(self, estilista_id):
        estilista = self.obtener_estilista(estilista_id)
        self.repository.eliminar(estilista)

    # --- Regla de negocio central: disponibilidad --------------------

    def validar_disponibilidad(self, estilista, fecha, hora):
        """
        Verifica que la estilista trabaje ese día de la semana y que
        la hora solicitada caiga dentro de su jornada laboral. Se
        usa desde el módulo de citas al agendar o reprogramar.
        """
        if not estilista.activo:
            raise ValidationDomainError(
                f'{estilista.nombre_completo} no está disponible actualmente.'
            )

        dia_semana = DIAS_SEMANA_ES[fecha.weekday()]
        if dia_semana not in estilista.dias_laborales:
            raise ValidationDomainError(
                f'{estilista.nombre_completo} no trabaja los días {dia_semana}.'
            )

        if not (estilista.hora_inicio_jornada <= hora <= estilista.hora_fin_jornada):
            raise ValidationDomainError(
                f'{estilista.nombre_completo} atiende entre '
                f'{estilista.hora_inicio_jornada} y {estilista.hora_fin_jornada}.'
            )

    # --- Reglas de negocio internas --------------------------------------

    def _validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValidationDomainError(
                'El nombre completo debe tener al menos 3 caracteres.'
            )

    def _validar_dias(self, dias):
        if not dias:
            raise ValidationDomainError('Debe indicar al menos un día laboral.')
        for dia in dias:
            if dia not in DIAS_SEMANA_ES:
                raise ValidationDomainError(f'"{dia}" no es un día válido.')

    def _validar_horario(self, inicio, fin):
        if not inicio or not fin:
            raise ValidationDomainError('Debe indicar hora de inicio y fin de jornada.')
        if inicio >= fin:
            raise ValidationDomainError('La hora de inicio debe ser menor que la de fin.')
