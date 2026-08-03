"""
Capa de APLICACION (API REST) del modulo de resenas.

Igual que en citas y servicios: el serializer valida el FORMATO, el
ResenaService (dominio) aplica las reglas de NEGOCIO (cita atendida,
resena unica por cita), y esta clase solo traduce entre HTTP y el
dominio.
"""

from rest_framework import viewsets
from rest_framework.response import Response

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .serializers import ResenaSerializer
from .services import ResenaService


class ResenaViewSet(viewsets.ViewSet):
    """
    GET    /api/resenas/       -> listar (filtros: ?puntuacion=, ?estilista=)
    POST   /api/resenas/       -> crear reseña
    GET    /api/resenas/{id}/  -> detalle
    PUT/PATCH /api/resenas/{id}/ -> actualizar
    DELETE /api/resenas/{id}/  -> eliminar
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ResenaService()

    def list(self, request):
        puntuacion = request.query_params.get('puntuacion')
        estilista = request.query_params.get('estilista')

        resenas = self.service.listar_resenas(puntuacion=puntuacion, estilista=estilista)
        serializer = ResenaSerializer(resenas, many=True)
        return Response({'count': resenas.count(), 'results': serializer.data})

    def retrieve(self, request, pk=None):
        try:
            resena = self.service.obtener_resena(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)
        return Response(ResenaSerializer(resena).data)

    def create(self, request):
        serializer = ResenaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # validacion de FORMATO

        try:
            resena = self.service.crear_resena(serializer.validated_data)  # reglas de NEGOCIO
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'La reseña ha sido registrada correctamente', 'data': ResenaSerializer(resena).data},
            status=201,
        )

    def update(self, request, pk=None):
        try:
            instancia = self.service.obtener_resena(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        parcial = request.method == 'PATCH'
        serializer = ResenaSerializer(instancia, data=request.data, partial=parcial)
        serializer.is_valid(raise_exception=True)

        try:
            resena = self.service.actualizar_resena(pk, serializer.validated_data)
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response({'mensaje': 'Reseña actualizada correctamente', 'data': ResenaSerializer(resena).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        try:
            resena = self.service.obtener_resena(pk)
            cliente = resena.cita.nombre_cliente
            self.service.eliminar_resena(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response({'mensaje': f'Reseña de "{cliente}" eliminada correctamente'})
