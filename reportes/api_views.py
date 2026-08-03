"""
Capa de APLICACION (API REST) del modulo de reportes.

A diferencia de los demas modulos, aqui no hay create/update/destroy:
todo es de SOLO LECTURA (GET). Por eso se usan APIView individuales
en vez de un ViewSet con router, ya que cada endpoint representa un
reporte distinto y no operaciones CRUD sobre un mismo recurso.
"""

from rest_framework.response import Response
from rest_framework.views import APIView

from .services import ReporteService


class IngresosView(APIView):
    """GET /api/reportes/ingresos/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD"""

    def get(self, request):
        service = ReporteService()
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        return Response(service.ingresos_por_rango(fecha_inicio, fecha_fin))


class IngresosPorCategoriaView(APIView):
    """GET /api/reportes/ingresos-por-categoria/"""

    def get(self, request):
        service = ReporteService()
        return Response(list(service.ingresos_por_categoria()))


class ServiciosMasSolicitadosView(APIView):
    """GET /api/reportes/servicios-mas-solicitados/?limite=5"""

    def get(self, request):
        service = ReporteService()
        limite = int(request.query_params.get('limite', 5))
        return Response(list(service.servicios_mas_solicitados(limite)))


class EstilistasMasSolicitadosView(APIView):
    """GET /api/reportes/estilistas-mas-solicitados/?limite=5"""

    def get(self, request):
        service = ReporteService()
        limite = int(request.query_params.get('limite', 5))
        return Response(list(service.estilistas_mas_solicitados(limite)))


class SatisfaccionView(APIView):
    """GET /api/reportes/satisfaccion/"""

    def get(self, request):
        service = ReporteService()
        return Response(service.satisfaccion_promedio())


class CitasPorEstadoView(APIView):
    """GET /api/reportes/citas-por-estado/"""

    def get(self, request):
        service = ReporteService()
        return Response(list(service.resumen_citas_por_estado()))


class DashboardView(APIView):
    """GET /api/reportes/dashboard/ -> resumen consolidado con las metricas clave"""

    def get(self, request):
        service = ReporteService()
        return Response(service.dashboard_general())
