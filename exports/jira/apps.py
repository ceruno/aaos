from django.apps import AppConfig


class JiraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exports.jira"
    label = "exports_jira"
