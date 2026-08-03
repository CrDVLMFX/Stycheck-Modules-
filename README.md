# Stycheck - Servicios Web y API REST (Evidencia AA5-EV03)

Sistema web y API REST para el salón de belleza Stycheck. Incluye la gestión del catálogo de servicios (RF08/RF09) y el agendamiento de citas (RF10/RF11).

## Arquitectura por Capas

El proyecto está estructurado en tres capas independientes:

1. Aplicación (views.py, api_views.py, forms.py, serializers.py): Recibe las peticiones HTTP, valida el formato de datos y responde al cliente.
2. Dominio (services.py): Contiene las reglas de negocio de manera independiente de la interfaz web o API.
3. Acceso a Datos (repositories.py): Encargado exclusivo de las operaciones con la base de datos a través del ORM.

Tanto la interfaz web como la API REST comparten la misma capa de servicios.

## API REST

Base: http://127.0.0.1:8000/api/

- Servicios (/api/servicios/): CRUD completo para la gestión de catálogo.
- Citas (/api/citas/): CRUD completo y endpoint /api/citas/{id}/cancelar/ para cancelar citas.

## Reglas de Negocio

- Agendamiento de citas con mínimo 2 horas de anticipación (zona horaria America/Bogota).
- Solo se permite agendar citas en servicios con estado activo.
- Validaciones de precios mayores a cero y duraciones válidas.

## Instalación y Ejecución

1. Instalar dependencias: pip install -r requirements.txt
2. Aplicar migraciones: python manage.py migrate
3. Iniciar servidor: python manage.py runserver

Rutas disponibles:
- Web: http://127.0.0.1:8000/servicios/ y http://127.0.0.1:8000/citas/
- API: http://127.0.0.1:8000/api/servicios/ y http://127.0.0.1:8000/api/citas/.
