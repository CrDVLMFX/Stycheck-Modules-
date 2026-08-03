"""
Capa de APLICACION (API REST) del modulo de citas.

Igual que en servicios: el serializer valida el FORMATO, el
CitaService (dominio) aplica las reglas de NEGOCIO (incluida la
anticipacion minima de 2 horas), y esta clase solo traduce entre
HTTP y el dominio.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .serializers import CitaSerializer
from .services import CitaService


class CitaViewSet(viewsets.ViewSet):
    """
    GET    /api/citas/               -> listar (filtros: ?estado=, ?estilista=, ?fecha=)
    POST   /api/citas/               -> agendar cita
    GET    /api/citas/{id}/          -> detalle
    PUT/PATCH /api/citas/{id}/       -> actualizar
    DELETE /api/citas/{id}/          -> eliminar definitivamente
    POST   /api/citas/{id}/cancelar/ -> cancelar (cambia estado, no borra)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CitaService()

    def list(self, request):
        estado = request.query_params.get('estado')
        estilista = request.query_params.get('estilista')
        fecha = request.query_params.get('fecha')

        citas = self.service.listar_citas(estado=estado, estilista=estilista, fecha=fecha)
        serializer = CitaSerializer(citas, many=True)
        return Response({'count': citas.count(), 'results': serializer.data})

    def retrieve(self, request, pk=None):
        try:
            cita = self.service.obtener_cita(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)
        return Response(CitaSerializer(cita).data)

    def create(self, request):
        serializer = CitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # validacion de FORMATO

        try:
            cita = self.service.crear_cita(serializer.validated_data)  # reglas de NEGOCIO
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'La cita ha sido registrada correctamente', 'data': CitaSerializer(cita).data},
            status=201,
        )

    def update(self, request, pk=None):
        try:
            instancia = self.service.obtener_cita(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        parcial = request.method == 'PATCH'
        serializer = CitaSerializer(instancia, data=request.data, partial=parcial)
        serializer.is_valid(raise_exception=True)

        try:
            cita = self.service.actualizar_cita(pk, serializer.validated_data)
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response({'mensaje': 'Cita actualizada correctamente', 'data': CitaSerializer(cita).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        try:
            cita = self.service.obtener_cita(pk)
            nombre = cita.nombre_cliente
            self.service.eliminar_cita(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response({'mensaje': f'Cita de "{nombre}" eliminada correctamente'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        try:
            cita = self.service.cancelar_cita(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response(
            {'mensaje': f'La cita de {cita.nombre_cliente} fue cancelada', 'data': CitaSerializer(cita).data}
        )
