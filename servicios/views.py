"""
Capa de APLICACION (vistas HTML) del catalogo de servicios.

Solo coordina: recibe la request, usa el formulario para validar el
FORMATO, delega en ServicioService las reglas de NEGOCIO y la
persistencia, y decide que plantilla renderizar. Nunca llama
directamente al ORM ni a form.save().
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from stycheck.exceptions import NotFoundError, ValidationDomainError

from .forms import ServicioForm
from .models import Servicio
from .services import ServicioService

service = ServicioService()


def listar_servicios(request):
    categoria = request.GET.get('categoria')
    servicios_list = service.listar_servicios(categoria=categoria)

    paginator = Paginator(servicios_list, 10)
    pagina = request.GET.get('page')
    servicios = paginator.get_page(pagina)

    return render(
        request,
        'servicios/lista.html',
        {
            'servicios': servicios,
            'categorias': Servicio.CATEGORIA_CHOICES,
            'categoria_actual': categoria,
        },
    )


def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            try:
                service.crear_servicio(form.cleaned_data)
                messages.success(request, 'Servicio creado correctamente.')
                return redirect('listar_servicios')
            except ValidationDomainError as error:
                form.add_error(None, str(error))
    else:
        form = ServicioForm()

    return render(
        request,
        'servicios/formulario.html',
        {'form': form, 'titulo': 'Nuevo servicio'},
    )


def editar_servicio(request, pk):
    try:
        servicio = service.obtener_servicio(pk)
    except NotFoundError:
        messages.error(request, 'El servicio solicitado no existe.')
        return redirect('listar_servicios')

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            try:
                service.actualizar_servicio(pk, form.cleaned_data)
                messages.success(request, 'Servicio actualizado correctamente.')
                return redirect('listar_servicios')
            except ValidationDomainError as error:
                form.add_error(None, str(error))
    else:
        form = ServicioForm(instance=servicio)

    return render(
        request,
        'servicios/formulario.html',
        {'form': form, 'titulo': f'Editar: {servicio.nombre}'},
    )


def eliminar_servicio(request, pk):
    try:
        servicio = service.obtener_servicio(pk)
    except NotFoundError:
        messages.error(request, 'El servicio solicitado no existe.')
        return redirect('listar_servicios')

    if request.method == 'POST':
        nombre = servicio.nombre
        service.eliminar_servicio(pk)
        messages.success(request, f'Servicio "{nombre}" eliminado.')

    return redirect('listar_servicios')
