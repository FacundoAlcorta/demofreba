# FREBA Backend - Base Tecnica Inicial

Backend Django/DRF preparado para arrancar desarrollo de dominio en una siguiente fase, con foco en una base tecnica limpia y mantenible.

## Estado actual

Implementado en esta etapa:

- estructura de settings separada por entorno (`base`, `local`, `prod`)
- carga de variables de entorno desde `.env`
- integracion base de DRF y CORS
- endpoint tecnico de salud: `GET /health/`
- base minima para testing con `pytest` + `pytest-django`
- configuracion de base de datos por `DATABASE_URL` (lista para PostgreSQL)

No implementado aun:

- apps de dominio (`organizations`, `communication_config`, `communications`, `documents`, `chats`, `expedients`, `audit`)
- modelos funcionales del negocio
- endpoints de negocio

## Requisitos

- Python 3.13+
- pip

## Instalacion

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracion de entorno

1. Copiar el ejemplo:

```bash
copy .env.example .env
```

2. Variables minimas relevantes:

- `DJANGO_SETTINGS_MODULE` (default recomendado: `config.settings.local`)
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `CORS_ALLOWED_ORIGINS`
- `CORS_ALLOW_ALL_ORIGINS`

### DATABASE_URL

Ejemplo PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/freba_backend
```

Si no se define `DATABASE_URL`, la configuracion local cae en `sqlite` automaticamente.

## Comandos de desarrollo

Levantar servidor:

```bash
python manage.py runserver
```

Chequeo de proyecto:

```bash
python manage.py check
```

Migraciones:

```bash
python manage.py migrate
```

Endpoint de salud:

- `GET http://127.0.0.1:8000/health/`

## Testing

Correr tests:

```bash
pytest
```

Configuracion minima en `pytest.ini`:

- `DJANGO_SETTINGS_MODULE=config.settings.local`
- `testpaths=tests`

## Estructura tecnica actual

```text
freba-backend/
  config/
    settings/
      __init__.py
      base.py
      local.py
      prod.py
    asgi.py
    urls.py
    views.py
    wsgi.py
  tests/
    test_health.py
  .env.example
  .gitignore
  manage.py
  pytest.ini
  requirements.txt
```

## Decisiones tecnicas tomadas en esta etapa

- settings modularizados por entorno
- lectura de entorno con `python-dotenv`
- parseo de `DATABASE_URL` con `dj-database-url`
- DRF y CORS instalados desde base tecnica
- endpoint `/health/` simple y sin acoplamiento a dominio
- testing base con `pytest` preparado

## Decision sobre custom user model

En esta etapa **no** se creo `AUTH_USER_MODEL` custom para evitar introducir una app de dominio antes de tiempo.

Decision explicita para la proxima fase:

- definir `AUTH_USER_MODEL` **antes de crear cualquier modelo de negocio** y antes de migraciones de dominio, para evitar retrabajo y migraciones complejas.

