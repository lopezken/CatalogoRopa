# tienda_ropa/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# --- CONFIGURACIÓN DE SEGURIDAD ---
# La SECRET_KEY se lee de una variable de entorno en Render.
# La segunda parte es una clave por defecto SOLO para desarrollo local.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-tu-clave-secreta-local')

# El modo DEBUG se desactiva automáticamente en Render.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Los hosts permitidos se configuran automáticamente en Render.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # Permitir acceso local si no estamos en Render
    ALLOWED_HOSTS.append('127.0.0.1')


# --- APLICACIONES Y MIDDLEWARE ---
INSTALLED_APPS = [
    'inventario',  # Tu app principal
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware de WhiteNoise para servir archivos estáticos eficientemente
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda_ropa.urls'

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

WSGI_APPLICATION = 'tienda_ropa.wsgi.application'


# --- BASE DE DATOS ---
# Usa la base de datos de Render (PostgreSQL) si está disponible,
# si no, usa la base de datos local (SQLite) para desarrollo.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'es-ni' # Español de Nicaragua
TIME_ZONE = 'America/Managua'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (CSS, JavaScript, imágenes del admin) ---
STATIC_URL = '/static/'
# Esta configuración es para que WhiteNoise funcione correctamente en producción.
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- ARCHIVOS MEDIA (Imágenes subidas por el usuario) ---
MEDIA_URL = '/media/'
# En desarrollo, los archivos se guardan localmente.
if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# En producción (Render), se usa Amazon S3.
else:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# --- CONFIGURACIÓN POR DEFECTO DE CLAVE PRIMARIA ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'