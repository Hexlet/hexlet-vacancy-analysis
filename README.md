# hexlet-vacancy-analysis   
.

## Requirements:

To run this project, you need to have the following software installed:
- Python >=3.12
- Uv
- PostgreSQL

## Preparation:

Create .env file with code kind of:
```bash
SECRET_KEY=your_secret_key
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
ALLOWED_HOSTS=127.0.0.1,localhost,yourdomain.com

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=secret123
EMAIL_TIMEOUT=10

DEBUG=True
```

Create a PostgreSQL user (or reuse an existing one) and a database using the parameters from DATABASE_URL.

## Installation:

To set up the project, navigate to the project directory and run the following commands:
```bash
make install
```
```bash
make migrate
```
```bash
make create-superuser
```

## Local run:

```bash
make run
```
.
## Comments