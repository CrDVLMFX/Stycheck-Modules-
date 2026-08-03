from django.urls import include, path
from rest_framework.routers import DefaultRouter

from citas.api_views import CitaViewSet
from servicios.api_views import ServicioViewSet
from resenas.api_views import ResenaViewSet
from clientes.api_views import ClienteViewSet
from estilistas.api_views import EstilistaViewSet
from reportes.api_views import (
    CitasPorEstadoView,
    DashboardView,
    EstilistasMasSolicitadosView,
    IngresosPorCategoriaView,
    IngresosView,
    SatisfaccionView,
    ServiciosMasSolicitadosView,
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='api-clientes')
router.register(r'servicios', ServicioViewSet, basename='api-servicios')
router.register(r'estilistas', EstilistaViewSet, basename='api-estilistas')
router.register(r'citas', CitaViewSet, basename='api-citas')
router.register(r'resenas', ResenaViewSet, basename='api-resenas')

urlpatterns = [
    path('', include(router.urls)),
    # Reportes: son de solo lectura, por eso van como rutas explicitas
    # y no como un ViewSet registrado en el router (no tienen CRUD).
    path('reportes/dashboard/', DashboardView.as_view(), name='api-reporte-dashboard'),
    path('reportes/ingresos/', IngresosView.as_view(), name='api-reporte-ingresos'),
    path('reportes/ingresos-por-categoria/', IngresosPorCategoriaView.as_view(), name='api-reporte-ingresos-categoria'),
    path('reportes/servicios-mas-solicitados/', ServiciosMasSolicitadosView.as_view(), name='api-reporte-servicios-top'),
    path('reportes/estilistas-mas-solicitados/', EstilistasMasSolicitadosView.as_view(), name='api-reporte-estilistas-top'),
    path('reportes/satisfaccion/', SatisfaccionView.as_view(), name='api-reporte-satisfaccion'),
    path('reportes/citas-por-estado/', CitasPorEstadoView.as_view(), name='api-reporte-citas-estado'),
]
