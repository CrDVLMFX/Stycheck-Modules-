"""
Formulario HTML de Cita.

IMPORTANTE: solo define los campos y su formato/apariencia. La regla
de negocio de "minimo 2 horas de anticipacion" y las demas
validaciones viven en citas/services.py (CitaService). La vista
nunca llama a form.save(): siempre pasa por el CitaService.
"""

from django import forms

from .models import Cita


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'nombre_cliente',
            'servicio',
            'estilista',
            'fecha',
            'hora',
            'estado',
        ]
        widgets = {
            'nombre_cliente': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej. María López'}
            ),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'estilista': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre_cliente': 'Nombre del cliente',
            'servicio': 'Servicio',
            'estilista': 'Estilista',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'estado': 'Estado',
        }
