"""
Capa de APLICACION (vistas HTML) del modulo de citas.

Solo coordina: valida el FORMATO con el formulario, delega en
CitaService las reglas de NEGOCIO y la persistencia, y decide que
plantilla renderizar.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .forms import CitaForm
from .models import Cita
from .services import CitaService

service = CitaService()


def listar_citas(request):
    estado = request.GET.get('estado')
    citas_list = service.listar_citas(estado=estado)

    paginator = Paginator(citas_list, 10)
    pagina = request.GET.get('page')
    citas = paginator.get_page(pagina)

    return render(
        request,
        'citas/lista.html',
        {
            'citas': citas,
            'estados': Cita.ESTADO_CHOICES,
            'estado_actual': estado,
        },
    )


def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            try:
                service.crear_cita(form.cleaned_data)
                messages.success(request, 'Cita agendada correctamente.')
                return redirect('listar_citas')
            except ValidationDomainError as error:
                form.add_error(None, str(error))
    else:
        form = CitaForm(initial={'estado': 'pendiente'})

    return render(
        request,
        'citas/formulario.html',
        {'form': form, 'titulo': 'Nueva cita'},
    )


def editar_cita(request, pk):
    try:
        cita = service.obtener_cita(pk)
    except NotFoundError:
        messages.error(request, 'La cita solicitada no existe.')
        return redirect('listar_citas')

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                service.actualizar_cita(pk, form.cleaned_data)
                messages.success(request, 'Cita actualizada correctamente.')
                return redirect('listar_citas')
            except ValidationDomainError as error:
                form.add_error(None, str(error))
    else:
        form = CitaForm(instance=cita)

    return render(
        request,
        'citas/formulario.html',
        {'form': form, 'titulo': f'Editar cita de {cita.nombre_cliente}'},
    )


def cancelar_cita(request, pk):
    try:
        cita = service.cancelar_cita(pk)
        if request.method == 'POST':
            messages.success(request, f'La cita de {cita.nombre_cliente} fue cancelada.')
    except NotFoundError:
        messages.error(request, 'La cita solicitada no existe.')

    return redirect('listar_citas')


def eliminar_cita(request, pk):
    try:
        cita = service.obtener_cita(pk)
    except NotFoundError:
        messages.error(request, 'La cita solicitada no existe.')
        return redirect('listar_citas')

    if request.method == 'POST':
        nombre = cita.nombre_cliente
        service.eliminar_cita(pk)
        messages.success(request, f'Cita de "{nombre}" eliminada.')

    return redirect('listar_citas')
