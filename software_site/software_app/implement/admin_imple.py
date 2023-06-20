'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 23:21:27
FilePath: \software_site\software_app\implement\admin_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.service.jwt_tools import RequestContext, preprocess_token, Role, RetCode
from software_app.implement.util.validator import validate, ValidationError
from software_app.service.simple_query import get_pile_status, update_pile_status, get_all_piles_status
from software_app.models import PileStatus, PileType
from software_app.service.schd import Scheduler, scheduler
from software_app.service.exceptions import PileDoesNotExisted
from software_app.service import simple_query
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
            'errmsg': "chargingPileId 应为一个数字"
        },
        'status': {
            'type': 'string',
            'enum': ['RUNNING', 'SHUTDOWN', 'UNAVAILABLE'],
            'errmsg': "status 应为可选值为'RUNNING', 'SHUTDOWN', 'UNAVAILABLE'的字符串"        
        }
    }
}

# 更新充电桩状态
@preprocess_token(limited_role=Role.ADMIN)
def update_pile_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
# def update_pile_api( req: HttpRequest) -> JsonResponse:
    # print("req", req)
    try:
        loads = validate(req, method='PUT', schema=__update_pile_schema__)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data': {}
        })
    # print("loads", loads)
    chargingPileId = int(loads['chargingPileId'])
    status = PileStatus[loads['status']]
    try:
        status_before = get_pile_status(chargingPileId)
        update_pile_status(chargingPileId, status)
        if status_before==PileStatus.RUNNING:
            if status==PileStatus.SHUTDOWN or status==PileStatus.UNAVAILABLE:
                scheduler.brake(chargingPileId)
        elif status_before==PileStatus.SHUTDOWN or status_before==PileStatus.UNAVAILABLE:
            if status==PileStatus.RUNNING:
                scheduler.recover(chargingPileId)
                pass
    except PileDoesNotExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data': {}
        })
    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'chargingPileId': chargingPileId,
            'status': status.name
        }
    })


# 查看报表
@preprocess_token(limited_role=Role.ADMIN)
def query_report_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
# def query_report_api(req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    report = simple_query.query_report()
    print(report)
    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': report
    })


# 查看所有充电桩状态
@preprocess_token(limited_role=Role.ADMIN)
def query_all_piles_stat_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
# def query_all_piles_stat_api(req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value, 
            'message': str(e),
            'data':{}
        })

    status_list = get_all_piles_status()

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': status_list
    })


# 查看总体排队情况
@preprocess_token(limited_role=Role.ADMIN)
def query_queue_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
# def query_queue_api(req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data':{}
        })

    snapshot = scheduler.snapshot()

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': snapshot
    })


if __name__ == "__main__":
    update_pile_api(None, None)