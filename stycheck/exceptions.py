"""
Excepciones de la capa de DOMINIO.

Estas excepciones representan errores de reglas de negocio. No saben
nada de HTTP, Django REST Framework ni de la base de datos: es tarea
de la capa de aplicación (vistas / api_views) traducirlas a una
respuesta (JSON, HTML, código de estado, etc).
"""


class DomainError(Exception):
    """Excepción base para cualquier error de la capa de dominio."""


class ValidationDomainError(DomainError):
    """Se lanza cuando un dato no cumple una regla de negocio."""


class NotFoundError(DomainError):
    """Se lanza cuando un recurso solicitado no existe."""
