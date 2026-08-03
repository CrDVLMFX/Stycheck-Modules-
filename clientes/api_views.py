"""
Capa de APLICACION (API REST) del modulo de clientes.

Igual que en servicios, citas y resenas: el serializer valida el
FORMATO, el ClienteService (dominio) aplica las reglas de NEGOCIO
(telefono valido, email unico), y esta clase solo traduce entre HTTP
y el dominio.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .serializers import ClienteSerializer
from .services import ClienteService


class ClienteViewSet(viewsets.ViewSet):
    """
    GET    /api/clientes/                -> listar (filtros: ?activo=, ?buscar=)
    POST   /api/clientes/                -> registrar cliente
    GET    /api/clientes/{id}/           -> detalle
    PUT/PATCH /api/clientes/{id}/        -> actualizar
    DELETE /api/clientes/{id}/           -> eliminar definitivamente
    POST   /api/clientes/{id}/desactivar/ -> baja logica (no borra)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClienteService()

    def list(self, request):
        activo = request.query_params.get('activo')
        if activo is not None:
            activo = activo.lower() in ('1', 'true', 'si')
        buscar = request.query_params.get('buscar')

        clientes = self.service.listar_clientes(activo=activo, buscar=buscar)
        serializer = ClienteSerializer(clientes, many=True)
        return Response({'count': clientes.count(), 'results': serializer.data})

    def retrieve(self, request, pk=None):
        try:
            cliente = self.service.obtener_cliente(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)
        return Response(ClienteSerializer(cliente).data)

    def create(self, request):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # validacion de FORMATO

        try:
            cliente = self.service.crear_cliente(serializer.validated_data)  # reglas de NEGOCIO
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'El cliente ha sido registrado correctamente', 'data': ClienteSerializer(cliente).data},
            status=201,
        )

    def update(self, request, pk=None):
        try:
            instancia = self.service.obtener_cliente(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        parcial = request.method == 'PATCH'
        serializer = ClienteSerializer(instancia, data=request.data, partial=parcial)
        serializer.is_valid(raise_exception=True)

        try:
            cliente = self.service.actualizar_cliente(pk, serializer.validated_data)
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response({'mensaje': 'Cliente actualizado correctamente', 'data': ClienteSerializer(cliente).data})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        try:
            cliente = self.service.obtener_cliente(pk)
            nombre = cliente.nombre_completo
            self.service.eliminar_cliente(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response({'mensaje': f'Cliente "{nombre}" eliminado correctamente'})

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        try:
            cliente = self.service.desactivar_cliente(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response(
            {'mensaje': f'El cliente {cliente.nombre_completo} fue desactivado', 'data': ClienteSerializer(cliente).data}
        )
