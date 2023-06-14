'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-24 22:51:29
FilePath: \software_site\software_app\implement\generic_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.service.jwt_tools import RequestContext
from software_app.implement.util.validator import validate, ValidationError
from software_app.service.jwt_tools import RequestContext, preprocess_token, Role, RetCode
from software_app.service.exceptions import UserAlreadyExisted, UserDoesNotExisted
from software_app.service.auth import register, login
from software_app.service.timemock import get_datetime_now, get_timestamp_now
from software_app.service.exceptions import WrongPassword
# /register 注册发送的json格式
__register_schema__ = {
    'type': 'object',
    'required': ['username', 'password'],
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 4,
            'maxLength': 20,
            'errmsg': "username 应为字符串(4~20)"
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 32,
            'errmsg': "password 应为字符串(8~32)"
        },
        'key': {
            'type': 'string',
            'maxLength': 32,
            'errmsg': "key 应为字符串(8~32)"
        }
    }
}


# /login 登录发送的json格式
__login_schema__ = {
    'type': 'object',
    'required': ['username', 'password'],
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 4,
            'maxLength': 20,
            'errmsg': "username 应为字符串(4~20)"
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 32,
            'errmsg': "password 应为字符串(8~32)"
        }
    }
}


def register_api(req: HttpRequest) -> JsonResponse:
    print("enter register_api")
    try:
        loads = validate(req, schema=__register_schema__)
        print(loads)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data':{}
        })
    username = loads['username']
    password = loads['password']
    if 'key' in loads:
        key = loads['key']
        if key=="":
            key=None
    else:
        key = None
    try:
        register(username, password, key)
    except UserAlreadyExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data':{}
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data':{}
    })


def login_api(req: HttpRequest) -> JsonResponse:
    try:
        loads = validate(req, schema=__login_schema__)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })
    username = loads['username']
    password = loads['password']
    try:
        token, role = login(username, password)
    except UserDoesNotExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data':{}
        })
    except WrongPassword as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e),
            'data':{}
        })

    is_admin = False
    if role == Role.ADMIN:
        is_admin = True

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'token': token,
            "is_admin": is_admin
        }
    })


def query_time(req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'datetime': get_datetime_now(),
            'timestamp': get_timestamp_now()
        }
    })
