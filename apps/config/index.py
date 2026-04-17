import os

CONFIG = {
    "app": {
        "name": "eventmanagementsystem",
        "mode": os.getenv("MODE_ENV", "LOCAL"),
        "version": "1.0.0",
        "debug": os.getenv("APP_DEBUG", "True"),
        "secret_key": os.getenv("APP_SECRET_KEY", "django-insecure-secret-key"),
        "allowed_hosts": os.getenv("APP_ALLOWED_HOSTS", "localhost,127.0.0.1").split(","),
        "db": os.getenv("APP_DB", "postgres://postgres:Pass-word123!@localhost:5432/eventmanagementsystem"),
    },
    "jwt": {
        "secret_key": os.getenv("JWT_SECRET_KEY", None),
        "algorithm": "HS256",
        "access_token_lifetime": 60,  # minutes
        "refresh_token_lifetime": 1,  # days
    }
}