from django.apps import AppConfig


class ConsultationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'consultation_app'

# apps.py
from django.apps import AppConfig

class ConsultationAppConfig(AppConfig):
    name = 'consultation_app'

    def ready(self):
        import consultation_app.signals
