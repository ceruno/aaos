from django.apps import AppConfig


class PostgresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exports.postgres"
    label = "exports_postgres"
