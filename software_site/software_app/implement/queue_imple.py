'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 00:44:28
FilePath: \backEnd\software_site\software_app\implement\queue_imple.py
'''
from _decimal import Decimal
from django.http import HttpRequest, JsonResponse
from django.db import transaction

from software_app.implement.util.resp_tool import RetCode
from software_app.implement.util.validator import validate, ValidationError
from software_app.models import PileType
from software_app.service.exceptions import MappingNotExisted, IllegalUpdateAttemption
from software_app.service.jwt_tools import RequestContext, preprocess_token, Role

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

from software_app.service.schd import scheduler, StatusType


# @preprocess_token(limited_role=Role.ADMIN)
@preprocess_token(limited_role=Role.USER)
def info_api(context: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    requested_flag = False
    request_id = None
    pile_id = None
    position = -1

    try:
        request_id = scheduler.get_request_id_by_username(context.username)
        reqeust_status = scheduler.get_request_status(request_id)
        pile_id = reqeust_status.pile_id
        position = reqeust_status.position
    except MappingNotExisted:
        requested_flag = True

    if pile_id is None:
        place = 'waiting_area'
    else:
        place = pile_id
    if requested_flag:
        cur_state = StatusType.NOTCHARGING.name
    else:
        cur_state = reqeust_status.status.name

    if request_id is not None:
        request_id = str(request_id)

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'chargeId': request_id,
            'queueLen': position,
            'curState': cur_state,
            'place': str(place)
        }
    })


@preprocess_token(limited_role=Role.USER)
def change_api(context: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        kwargs = validate(req, schema=__change_schema__)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    charge_mode: str = kwargs['chargingMode']
    require_amount: Decimal = Decimal(kwargs['chargingAmount'])

    if charge_mode == 'T':
        request_mode = PileType.CHARGE
    elif charge_mode == 'F':
        request_mode = PileType.FAST_CHARGE

    try:
        request_id = scheduler.get_request_id_by_username(context.username)
        scheduler.update_request(request_id, require_amount,request_mode)
    except MappingNotExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })
    except IllegalUpdateAttemption as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        "data": {}
    })
