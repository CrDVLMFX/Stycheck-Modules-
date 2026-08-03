"""
Capa de APLICACION (API REST) del catalogo de servicios.

Su unica responsabilidad es traducir HTTP <-> dominio:
  1. Usa el serializer para validar el FORMATO de la entrada.
  2. Le pasa los datos ya tipados al servicio (dominio), que aplica
     las reglas de negocio y coordina la persistencia.
  3. Traduce el resultado (o la excepcion de dominio) a una respuesta HTTP.

No contiene reglas de negocio ni llama directamente al ORM.
"""

from rest_framework import viewsets
from rest_framework.response import Response

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .serializers import ServicioSerializer
from .services import ServicioService


class ServicioViewSet(viewsets.ViewSet):
    """
    GET    /api/servicios/          -> listar (filtros: ?categoria=, ?popular=)
    POST   /api/servicios/          -> crear
    GET    /api/servicios/{id}/     -> detalle
    PUT/PATCH /api/servicios/{id}/  -> actualizar
    DELETE /api/servicios/{id}/     -> eliminar
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ServicioService()

    def list(self, request):
        categoria = request.query_params.get('categoria')
        popular_param = request.query_params.get('popular')
        popular = popular_param.lower() in ('1', 'true') if popular_param is not None else None

        servicios = self.service.listar_servicios(categoria=categoria, popular=popular)
        serializer = ServicioSerializer(servicios, many=True)
        return Response({'count': servicios.count(), 'results': serializer.data})

    def retrieve(self, request, pk=None):
        try:
            servicio = self.service.obtener_servicio(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)
        return Response(ServicioSerializer(servicio).data)

    def create(self, request):
        serializer = ServicioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # validacion de FORMATO

        try:
            servicio = self.service.crear_servicio(serializer.validated_data)  # reglas de NEGOCIO
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'Servicio creado correctamente', 'data': ServicioSerializer(servicio).data},
            status=201,
        )

    def update(self, request, pk=None):
        try:
            instancia = self.service.obtener_servicio(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        parcial = request.method == 'PATCH'
        serializer = ServicioSerializer(instancia, data=request.data, partial=parcial)
        serializer.is_valid(raise_exception=True)

        try:
            servicio = self.service.actualizar_servicio(pk, serializer.validated_data)
        except ValidationDomainError as error:
            return Response({'mensaje': str(error)}, status=400)

        return Response(
            {'mensaje': 'Servicio actualizado correctamente', 'data': ServicioSerializer(servicio).data}
        )

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        try:
            servicio = self.service.obtener_servicio(pk)
            nombre = servicio.nombre
            self.service.eliminar_servicio(pk)
        except NotFoundError as error:
            return Response({'mensaje': str(error)}, status=404)

        return Response({'mensaje': f'Servicio "{nombre}" eliminado correctamente'})
