"""充电相关接口路由"""
from django.urls import path

import software_app.implement.charging_imple as charging_imple

urlpatterns = [
    path('request', charging_imple.request_api),  # 提交充电请求
    path('submit', charging_imple.submit_api),  # 结束充电
    path('remainAmount', charging_imple.remainAmount_api),  # 查询剩余充电量
    path('cancel', charging_imple.cancel_api),  # 处理取消充电请求
]
