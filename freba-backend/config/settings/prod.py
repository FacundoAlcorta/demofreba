from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403


DEBUG = env_bool("DEBUG", False)

if SECRET_KEY == "unsafe-dev-secret-key":
    raise ImproperlyConfigured(
        "SECRET_KEY no configurada. Defini una SECRET_KEY segura para produccion."
    )

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS no configurado. Defini al menos un host valido."
    )

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

