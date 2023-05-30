"""订单相关接口路由"""
from django.urls import path

import software_app.implement.charging_imple as charging_imple

urlpatterns = [
    path('charging', charging_imple.report_api),  # 查看充电详单
]
