from .base import *

DEBUG=True

# OTP_INPUT_LENGTH = 4

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

INTERNAL_IPS = ["127.0.0.1"]

# Passwords Validation
AUTH_PASSWORD_VALIDATORS = []