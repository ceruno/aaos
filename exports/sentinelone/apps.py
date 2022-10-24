from django.apps import AppConfig


class SentinelOneExportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exports.sentinelone"
    label = "exports_sentinelone"
