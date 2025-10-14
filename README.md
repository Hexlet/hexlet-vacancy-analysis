# hexlet-vacancy-analysis   
Project idea: A service that automatically collects job postings from key platforms (hh.ru, SuperJob, Habr Career, Telegram channels) and generates analytics on the IT job market. It will be a unified tool where users can see which professions are in demand, how salaries are changing, which skills are most frequently required by employers, and how these indicators evolve over time.

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
