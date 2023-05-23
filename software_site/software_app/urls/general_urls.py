"""general接口路由"""
from django.urls import path

import software_app.implement.generic_imple as generic_imple

urlpatterns = [
    path('register', generic_imple.register_api),
    path('login', generic_imple.login_api),
    path('time', generic_imple.query_time),
]
