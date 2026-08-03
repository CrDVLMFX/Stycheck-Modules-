"""
Configuración del proyecto Stycheck (Django).
Evidencia GA7-220501096-AA2-EV01 — módulo Servicios.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in (
    '1', 'true', 'yes'
)

# '*' solo para pruebas locales / demo en la misma red (celular, tablet, etc.)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'clientes',
    'servicios',
    'estilistas',
    'citas',
    'resenas',
    'reportes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stycheck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stycheck.wsgi.application'

# Base de datos: MySQL servido por Laragon.
# Ajusta USER/PASSWORD si tu servidor MySQL los requiere.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        )
    },
]

# Español + zona horaria de Colombia (mensajes de validación en español)
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-misuperclave_secreta_para_desarrollo_local_12345',
)
# Configuración de Django REST Framework (Requisito: API REST)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),
    'PAGE_SIZE': 10,

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}





