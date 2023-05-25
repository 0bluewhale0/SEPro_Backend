"""充电相关接口路由"""
from django.urls import path

import software_app.implement.charging_imple as charging_imple

urlpatterns = [
    path('request', charging_imple.request_api),  # ok
    path('submit', charging_imple.submit_api),  # ok
    path('remainAmount', charging_imple.remainAmount_api),  # ok
    path('cancel', charging_imple.cancel_api),  # ok
]
