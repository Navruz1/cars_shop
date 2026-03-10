from .base import *

# Security
DEBUG = False
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# OTP
OTP_INPUT_LENGTH = 6

# Cookies и SSL
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HTTP Security Headers
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Access to API
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default="", cast=Csv())

# POST Requests
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Redis, for Caches and Sessions
REDIS_HOST = env("REDIS_HOST", default="localhost")
REDIS_PORT = env("REDIS_PORT", default="6379", cast=int)
REDIS_DB = env("REDIS_DB", default="0", cast=int)

# Passwords Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        # максимальная допустимая схожесть (от 0 до 1) следующих атрибутов пользователя
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'first_name', 'last_name', 'email'),
            'max_similarity': 0.7,
        }
    },
    {
        # Минимальная длина пароля
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}  # рекомендуемая минимальная длина 12
    },
    {
        # Путь к файлу со списком часто используемых паролей
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # 'OPTIONS': {'password_list_path': BASE_DIR / '.../common-passwords.txt'},
    },
    {
        # Запрет на full-number пароли
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]