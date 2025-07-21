import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'DEBUG': os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),

    'DATABASE_ENGINE': os.getenv('DATABASE_ENGINE', 'sqlite3'),
    'DATABASE_NAME': os.getenv('DATABASE_NAME', 'postgres'),
    'DATABASE_USERNAME': os.getenv('DATABASE_USERNAME', 'postgres'),
    'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
    'DATABASE_HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
    'DATABASE_PORT': os.getenv('DATABASE_PORT', '5432'),

    'EMAIL_BACKEND': os.environ.get(
        'DJANGO_EMAIL_BACKEND',
        'django.core.mail.backends.console.EmailBackend'
        ),
    'EMAIL_HOST': os.environ.get("EMAIL_HOST", ""),
    'EMAIL_PORT': int(os.environ.get("EMAIL_PORT", 587)),
    'EMAIL_USE_TLS': os.getenv("EMAIL_USE_TLS", "true").lower() in ("true", "1", "yes"),
    'EMAIL_HOST_USER': os.environ.get("EMAIL_HOST_USER", ""),
    'EMAIL_HOST_PASSWORD': os.environ.get("EMAIL_HOST_PASSWORD", ""),
    'EMAIL_TIMEOUT': int(os.environ.get("EMAIL_TIMEOUT", 10)),

    'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(','),
    'SUPERJOB_API_KEY': os.getenv('SUPERJOB_API_KEY'),
}
