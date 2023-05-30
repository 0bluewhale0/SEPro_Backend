from django.apps import AppConfig

init_flag = True


class SoftwareAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'software_app'

    def ready(self) -> None:
        from software_app.service.schd import on_init
        on_init()
        global init_flag
        if init_flag is False:
            return
        init_flag = False
        from software_app.service.schd import on_init as on_schd_init
        on_schd_init()
