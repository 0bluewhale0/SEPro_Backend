'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 00:44:28
FilePath: \backEnd\software_site\software_app\implement\queue_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.servive.jwt import RequestContext

# /queue/change
# {
#     "chargingMode": "F",
#     "chargingAmount": "47.74"
# }
__change_schema__ = {
    'type': 'object',
    'required': ['chargingMode', 'chargingAmount'],
    'properties': {
        'chargingMode': {
            'type': 'string',
            'enum': ['T', 'F'],
            'errmsg': "charge_mode 应为可选值为'T'或'F'的字符串"
        },
        'chargingAmount': {
            'type': 'string',
            'pattern': r'\d+\.\d{2}',
            'errmsg': "chargingAmount 应为精度为2的浮点数"
        }
    }
}

# @preprocess_token(limited_role=Role.ADMIN)
def info_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass
    # try:
    #     validate(req, method='GET')
    # except ValidationError as e:
    #     return JsonResponse({
    #         'code': RetCode.FAIL.value,
    #         'message': str(e)
    #     })

    # snapshot = scheduler.snapshot()

    # return JsonResponse({
    #     'code': RetCode.SUCCESS.value,
    #     'message': 'success',
    #     'data': snapshot
    # })

def change_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass
