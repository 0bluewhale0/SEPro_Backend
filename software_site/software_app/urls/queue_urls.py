"""queue相关接口路由"""
from django.urls import path

import software_app.implement.queue_imple as queue_imple

urlpatterns = [
    path('change', queue_imple.change_api),
    path('info', queue_imple.info_api),
]
