"""
Formulario HTML de Servicio.

IMPORTANTE: solo define que campos se piden y su formato/apariencia
(widgets). Las reglas de NEGOCIO (nombre minimo, precio > 0, etc.)
viven en la capa de dominio: servicios/services.py. La vista nunca
llama a form.save(): siempre pasa por el ServicioService.
"""

from django import forms

from .models import Servicio


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'duracion_minutos',
            'precio',
            'popular',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej. Corte y estilo'}
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Describe brevemente el servicio',
                }
            ),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'duracion_minutos': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 5}
            ),
            'precio': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}
            ),
            'popular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del servicio',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'duracion_minutos': 'Duración (minutos)',
            'precio': 'Precio (COP)',
            'popular': '¿Servicio popular?',
            'activo': '¿Servicio activo?',
        }
