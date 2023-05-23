'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 00:57:38
FilePath: \backEnd\software_site\software_app\implement\charging_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.servive.jwt import RequestContext


# /charging/request 充电模式（快充/慢充），请求充电量（度数）发送的json格式

# {
#     "chargingMode": "F",
#     "chargingAmount": 45.56,
#     "batteryAmount": 66.67
# }

# 这里需要确保chargingAmount和batteryAmount的值精确到小数点后两位，但是schema无法实现，所以在实现函数中需要自己检查
__register_schema__ = {
    'type': 'object',
    'required': ['chargingMode', 'chargingAmount', 'batteryAmount'],
    'properties': {
        'chargingMode': {
            'type': 'string',
            'enum': ['T', 'F'],
            'errmsg': "charge_mode 应为可选值为'T'或'F'的字符串"
        },
        'chargingAmount': {
            'type': 'number',
            'errmsg': "chargingAmount 应为浮点数"
        },
        'batteryAmount': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 32,
            'errmsg': "batteryAmount 应为浮点数"
        }
    }
}

def request_api(req: HttpRequest) -> JsonResponse:
    pass

def submit_api(req: HttpRequest) -> JsonResponse:
    pass

def remainAmount_api(req: HttpRequest) -> JsonResponse:
    pass

def cancel_api(req: HttpRequest) -> JsonResponse:
    pass

def report_api(req: HttpRequest) -> JsonResponse:
    pass