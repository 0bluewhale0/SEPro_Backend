"""充电相关接口路由"""
from django.urls import path

import software_app.implement.charging_imple as charging_imple


urlpatterns = [
    path('request', charging_imple.request_api),
    path('submit', charging_imple.submit_api),
    path('remainAmount', charging_imple.remainAmount_api),
    path('cancel', charging_imple.cancel_api),
]
