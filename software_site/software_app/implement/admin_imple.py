'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-23 23:47:11
FilePath: \backEnd\software_site\software_app\implement\admin_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.service.jwt_tools import RequestContext


# {
#     "chargingPileId": 5,
#     "status": "RUNNING"
# }

# /admin/update-pile 更新充电桩状态发送的post json格式
__update_pile_schema__ = {
    'type': 'object',
    'required': ['chargingPileId', 'status'],
    'properties': {
        'chargingPileId': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 5,
            'errmsg': "chargingPileId 应为一个不大于5的数字"
        },
        'status': {
            'type': 'string',
            'enum': ['RUNNING', 'SHUTDOWN', 'UNAVAILABLE'],
            'errmsg': "status 应为可选值为'RUNNING', 'SHUTDOWN', 'UNAVAILABLE'的字符串"        
        }
    }
}

# 更新充电桩状态
def update_pile_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass

# 查看报表
def query_report_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass

# 查看所有充电桩状态
def query_all_piles_stat_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass

# 查看总体排队情况
def query_queue_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass