from django.apps import AppConfig


class SoftwareAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'software_app'

    def ready(self) -> None:
        from software_app.service.schd import on_init
        on_init()
