"""
Capa de APLICACION (API REST) del modulo de estilistas.

Igual que en los demas modulos: el serializer valida el FORMATO, el
EstilistaService (dominio) aplica las reglas de NEGOCIO, y esta
clase solo traduce entre HTTP y el dominio.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .serializers import EstilistaSerializer
from .services import EstilistaService


class EstilistaViewSet(viewsets.ViewSet):
    """
    GET    /api/estilistas/                -> listar (filtros: ?activo=, ?especialidad=, ?dia=)
    POST   /api/estilistas/                -> registrar estilista
    GET    /api/estilistas/{id}/           -> detalle
    PUT/PATCH /api/estilistas/{id}/        -> actualizar
    DELETE /api/estilistas/{id}/           -> eliminar definitivamente
    POST   /api/estilistas/{id}/desactivar/ -> baja logica
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = EstilistaService()

    def list(self, request):
        activo = request.query_params.get('activo')
        if activo is not None:
            activo = activo.lower() in ('1', 'true', 'si')
        especialidad = request.query_params.get('especialidad')
        dia = request.query_params.get('dia')

        estilistas = self.service.listar_estilistas(activo=activo, especialidad=especialidad, dia=dia)
        serializer = EstilistaSerializer(estilistas, many=True)
        return Response({'count': estilistas.count(), 'results': serializer.data})

    def retrieve(self, request, pk=None):
        try:
            estilista = self.service.obtener_estilista(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)
        return Response(EstilistaSerializer(estilista).data)

    def create(self, request):
        serializer = EstilistaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # validacion de FORMATO

        try:
            estilista = self.service.crear_estilista(serializer.validated_data)  # reglas de NEGOCIO
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'La estilista ha sido registrada correctamente', 'data': EstilistaSerializer(estilista).data},
            status=201,
        )

    def update(self, request, pk=None):
        try:
            instancia = self.service.obtener_estilista(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        parcial = request.method == 'PATCH'
        serializer = EstilistaSerializer(instancia, data=request.data, partial=parcial)
        serializer.is_valid(raise_exception=True)

        try:
            estilista = self.service.actualizar_estilista(pk, serializer.validated_data)
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response({'mensaje': 'Estilista actualizada correctamente', 'data': EstilistaSerializer(estilista).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        try:
            estilista = self.service.obtener_estilista(pk)
            nombre = estilista.nombre_completo
            self.service.eliminar_estilista(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response({'mensaje': f'Estilista "{nombre}" eliminada correctamente'})

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        try:
            estilista = self.service.desactivar_estilista(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response(
            {'mensaje': f'{estilista.nombre_completo} fue desactivada', 'data': EstilistaSerializer(estilista).data}
        )
