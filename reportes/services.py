"""
Capa de DOMINIO (Service) del módulo de reportes (RF13).

A diferencia de citas, servicios, clientes y reseñas, este módulo NO
tiene modelo ni tabla propia: no guarda datos, los LEE y los agrega.
Convierte los registros crudos de Cita, Servicio y Resena en
métricas de negocio (ingresos, popularidad, satisfacción).

Por eso no hay repositories.py: las consultas de agregación se hacen
directamente aquí con el ORM de Django (Sum, Count, Avg), ya que son
el corazón de este módulo y no simples lecturas CRUD.
"""

from datetime import date

from django.db.models import Avg, Count, DecimalField, Sum
from django.db.models.functions import Coalesce

from citas.models import Cita
from resenas.models import Resena
from servicios.models import Servicio

ESTADOS_QUE_GENERAN_INGRESO = ['confirmada']


class ReporteService:

    # --- Ingresos -----------------------------------------------------

    def ingresos_por_rango(self, fecha_inicio=None, fecha_fin=None):
        """
        Suma el precio del servicio de cada cita confirmada dentro del
        rango de fechas. Una cita solo cuenta como ingreso si ya fue
        atendida (estado 'confirmada'), no si está pendiente o cancelada.
        """
        citas = Cita.objects.filter(estado__in=ESTADOS_QUE_GENERAN_INGRESO)

        if fecha_inicio:
            citas = citas.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            citas = citas.filter(fecha__lte=fecha_fin)

        total = citas.aggregate(
            total=Coalesce(Sum('servicio__precio'), 0, output_field=DecimalField())
        )['total']

        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'citas_facturables': citas.count(),
            'ingresos_totales': total,
        }

    def ingresos_por_categoria(self):
        """Desglosa los ingresos por categoría de servicio (cabello, uñas, etc.)."""
        return (
            Cita.objects.filter(estado__in=ESTADOS_QUE_GENERAN_INGRESO)
            .values('servicio__categoria')
            .annotate(
                total_citas=Count('id'),
                ingresos=Coalesce(Sum('servicio__precio'), 0, output_field=DecimalField()),
            )
            .order_by('-ingresos')
        )

    # --- Popularidad ----------------------------------------------------

    def servicios_mas_solicitados(self, limite=5):
        """Top de servicios con más citas registradas (cualquier estado)."""
        return (
            Servicio.objects.annotate(total_citas=Count('citas'))
            .filter(total_citas__gt=0)
            .order_by('-total_citas')[:limite]
            .values('id', 'nombre', 'categoria', 'total_citas')
        )

    def estilistas_mas_solicitados(self, limite=5):
        """Top de estilistas por número de citas agendadas."""
        return (
            Cita.objects.values('estilista')
            .annotate(total_citas=Count('id'))
            .order_by('-total_citas')[:limite]
        )

    # --- Satisfacción -----------------------------------------------------

    def satisfaccion_promedio(self):
        """Promedio general de calificación y distribución por puntuación."""
        promedio = Resena.objects.aggregate(promedio=Avg('puntuacion'))['promedio']

        distribucion = (
            Resena.objects.values('puntuacion')
            .annotate(total=Count('id'))
            .order_by('puntuacion')
        )

        return {
            'promedio_general': round(promedio, 2) if promedio else None,
            'total_resenas': Resena.objects.count(),
            'distribucion': list(distribucion),
        }

    # --- Estado general de citas -----------------------------------------

    def resumen_citas_por_estado(self):
        """Cuántas citas hay en cada estado: pendiente, confirmada, cancelada."""
        return (
            Cita.objects.values('estado')
            .annotate(total=Count('id'))
            .order_by('estado')
        )

    # --- Dashboard consolidado --------------------------------------------

    def dashboard_general(self):
        """Un solo endpoint con las métricas clave para la pantalla principal."""
        return {
            'ingresos': self.ingresos_por_rango(),
            'servicios_mas_solicitados': list(self.servicios_mas_solicitados()),
            'satisfaccion': self.satisfaccion_promedio(),
            'citas_por_estado': list(self.resumen_citas_por_estado()),
            'generado': date.today(),
        }
