from django.urls import path

from . import views

urlpatterns = [
    path('', views.listar_servicios, name='listar_servicios'),
    path('nuevo/', views.crear_servicio, name='crear_servicio'),
    path('<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    path('<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
]
