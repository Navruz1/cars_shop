from pathlib import Path
from decouple import config, Csv  # pip install python-decouple

# Build paths: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config("SECRET_KEY", "")
DEBUG = config('DEBUG', 'True', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', '', cast=Csv()) # HOSTS=localhost,127.0.0.1 -> ['localhost', '127.0.0.1']

# Apps
INSTALLED_APPS = [

    # Native
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Installed
    'django_filters',
    'rest_framework',   # DRF
    'drf_spectacular',  # Swagger
    # 'drf_yasg',       # Swagger

    # Created
    'apps.cars',
    'apps.users'
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs and templates
ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': config("DB_NAME", BASE_DIR / "db.sqlite3"),
        'USER': config("DB_USER", ""),
        'PASSWORD': config("DB_PASSWORD", ""),
        'HOST': config("DB_HOST", "localhost"),
        'PORT': config("DB_PORT", "5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files / Media files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# API / Swagger
SPECTACULAR_SETTINGS = {    # Важно для работы Swagger-а с бинарными (медиа) файлами
    'TITLE': 'My API',
    'VERSION': '1.0.0',
    'COMPONENT_SPLIT_REQUEST': True,
}






