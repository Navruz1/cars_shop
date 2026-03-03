from pathlib import Path
from decouple import config as env, Csv
from datetime import timedelta # for token lifetime

# Build paths: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = env("SECRET_KEY", "")
DEBUG = env('DEBUG', 'True', cast=bool)
ALLOWED_HOSTS = env('ALLOWED_HOSTS', '', cast=Csv()) # HOSTS=localhost,127.0.0.1 -> ['localhost', '127.0.0.1']

# Apps
INSTALLED_APPS = [

    # Django Native
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Installed
    'django_filters',
    'rest_framework',   # DRF
    # 'drf_spectacular',  # Swagger
    'drf_yasg',

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
AUTH_USER_MODEL = "users.User"

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
        'ENGINE': env("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': env("DB_NAME", BASE_DIR / "db.sqlite3"),
        'USER': env("DB_USER", ""),
        'PASSWORD': env("DB_PASSWORD", ""),
        'HOST': env("DB_HOST", "localhost"),
        'PORT': env("DB_PORT", "5432"),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Asia/Tashkent" # 'UTC'
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
    # 'DEFAULT_SCHEMA_CLASS': (
    #     'drf_spectacular.openapi.AutoSchema',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}

# Tokens / Authenticate (JWT)
SIMPLE_JWT = {
    # Access / Refresh Tokens
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),    # Вр. жизни токена
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Вр. жизни refresh-а, который создаёт токены
    'ROTATE_REFRESH_TOKENS': True,      # Каждое исп. refresh генерирует новый refresh-токен
    'BLACKLIST_AFTER_ROTATION': True,   # Старые refresh-токены попадает в чёрный список
    'TOKEN_BLACKLIST_ENABLE': True,     # Аннулирование токенов при их краже или logout
    'JTI_CLAIM': 'jti',                 # jti - уникальный ID токена, используется для чёрного списка и ротации.
    'UPDATE_LAST_LOGIN': False,     # Не обновлять last_login при каждом новом токене, чтобы не перегружать БД

    # Sliding Tokens
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",       # Альтернатива access + refresh
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),         # Сколько живёт токен, прежде чем обновлять
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),    # Максимум времени для обновлений

    # Encryption
    'ALGORITHM': 'HS256',       # Алгоритм шифрования токенов
    'SIGNING_KEY': SECRET_KEY,  # Ключ, которым подписывается токен
    'VERIFYING_KEY': '',        # Для ассиметричного шифрования. Пустой, потому что HS256 симметричный

    # HTTP Headers
    'AUTH_HEADER_TYPES': ('Bearer',),           # Стандартный способ передачи токена (Bearer - носитель)
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',   # Название заголовка
    "USER_ID_FIELD": "id",                      # поле id модели User
    "USER_ID_CLAIM": "user_id",                 # id превратить в CLAIM в токене (user_id)
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    # Token Classes
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",), # какие токены будут использоваться для проверки
    "TOKEN_TYPE_CLAIM": "token_type",                                       # поле в токене для указания типа (access / refresh).
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",        # класс, который создаётся на основе токена, если пользователь не загружен полностью

    # Other Settings
    "ISSUER": None,    # От кого токен
    "AUDIENCE": None,  # К кому токен
    "JSON_ENCODER": None,   # Кастомный сериализатор JSON
    "JWK_URL": None,        # Для получения публичного ключа при JWKS
    "LEEWAY": 0,  # допустимое отклонение времени токена (сек) на компенсацию разницы времени на сервере

    # Token Serializers (for API)
    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API',
    'VERSION': '1.0.0',
    'SECURITY': [
        {
            'bearerAuth': [],
        }
    ],
    'COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    }
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": (
                "JWT Authorization header using the Bearer scheme.\n\n"
                "Example:\n"
                "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            ),
        }
    },
    "USE_SESSION_AUTH": False,  # отключаем Basic auth
}


# API / Swagger
# SPECTACULAR_SETTINGS = { # Важно для работы Swagger с бинарными (медиа) файлами
#     'TITLE': 'My API',
#     'VERSION': '1.0.0',
#     'COMPONENT_SPLIT_REQUEST': True,
# }





