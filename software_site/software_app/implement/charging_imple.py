'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 00:57:38
FilePath: \backEnd\software_site\software_app\implement\charging_imple.py
'''
from _decimal import Decimal
from django.http import HttpRequest, JsonResponse
from django.db import transaction

from software_app.implement.util.resp_tool import RetCode
from software_app.implement.util.validator import validate, ValidationError
from software_app.models import PileType, Order
from software_app.service.exceptions import AlreadyRequested, OutOfSpace, MappingNotExisted
from software_app.service.jwt_tools import RequestContext, preprocess_token, Role

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
            'type': 'number',
            'errmsg': "batteryAmount 应为浮点数"
        }
    }
}

from software_app.service.schd import scheduler
from software_app.service.simple_query import get_all_orders
from software_app.service.timemock import get_timestamp_now


@preprocess_token(limited_role=Role.USER)
def request_api(context: RequestContext, req: HttpRequest) -> JsonResponse:  # 处理充电请求
    try:
        kwargs = validate(req, schema=__register_schema__)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    chargingMode: str = kwargs['chargingMode']
    chargingAmount: Decimal = Decimal(kwargs['chargingAmount'])
    batteryAmount: Decimal = Decimal(kwargs['batteryAmount'])

    if chargingMode == 'T':
        request_mode = PileType.CHARGE
    elif chargingMode == 'F':
        request_mode = PileType.FAST_CHARGE

    try:
        scheduler.submit_request(
            request_mode, context.username, chargingAmount, batteryAmount)
    except AlreadyRequested as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })
    except OutOfSpace as e:
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


@preprocess_token(limited_role=Role.USER)
def submit_api(context: RequestContext, req: HttpRequest) -> JsonResponse:  # 结束充电
    try:
        validate(req)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    try:
        request_id = scheduler.get_request_id_by_username(context.username)
        order: Order = scheduler.end_request(request_id, return_order=True)
    except MappingNotExisted as e:
        #判断是否充电结束
        order  = scheduler.checkCache(context.username)
        if order is not None:
            return JsonResponse({
                'code': RetCode.SUCCESS.value,
                'message': 'success',
                "data": {
                    "userId": int(order.user_id),
                    "orderId": str(order.order_id),
                    "createTime": str(order.create_time),
                    "chargingPileId": str(order.pile_id),
                    "volume": round(order.charged_amount, 2),
                    "chargingTime": order.charged_time,
                    "startTime": str(order.begin_time),
                    "endTime": str(order.end_time),
                    "chargingFee": round(order.charging_cost, 2),
                    "serviceFee": round(order.service_cost, 2),
                    "totalFee": round(order.total_cost, 2),
                    "time": str(get_timestamp_now())
                }
            })
        else:
            return JsonResponse({
                'code': RetCode.FAIL.value,
                'message': str(e),
                "data": {}
            })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        "data": {
            "userId": int(order.user_id),
            "orderId": str(order.order_id),
            "createTime": str(order.create_time),
            "chargingPileId": str(order.pile_id),
            "volume": round(order.charged_amount, 2),
            "chargingTime": order.charged_time,
            "startTime": str(order.begin_time),
            "endTime": str(order.end_time),
            "chargingFee": round(order.charging_cost, 2),
            "serviceFee": round(order.service_cost, 2),
            "totalFee": round(order.total_cost, 2),
            "time": str(get_timestamp_now())
        }
    })


@preprocess_token(limited_role=Role.USER)
def remainAmount_api(context: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    try:
        request_id = scheduler.get_request_id_by_username(context.username)
        left_amount = scheduler.query_left_amount(request_id)
    except MappingNotExisted as e:
        order = scheduler.checkCache(context.username)
        if order is not None:
            return JsonResponse({
                'code': RetCode.SUCCESS.value,
                'message': 'success',
                "data": {
                    "amount": 0.0
                }
            })
        else:
            return JsonResponse({
                'code': RetCode.FAIL.value,
                'message': str(e),
                "data": {}
            })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        "data": {
            "amount": left_amount
        }
    })


@preprocess_token(limited_role=Role.USER)
def cancel_api(context: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    try:
        request_id = scheduler.get_request_id_by_username(context.username)
        scheduler.end_request(request_id)
    except MappingNotExisted as e:
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


@preprocess_token(limited_role=Role.USER)
def report_api(context: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            "data": {}
        })

    username = context.username
    orders = get_all_orders(username)
    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': orders
    })
