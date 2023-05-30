from django.apps import AppConfig

init_flag = True
# init_flag = False


class SoftwareAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'software_app'

    def ready(self) -> None:
        global init_flag
        if init_flag is False:
            return
        init_flag = False
        from software_app.service.auth import init_pileModels
        init_pileModels()
        from software_app.service.schd import on_init as on_schd_init
        on_schd_init()
