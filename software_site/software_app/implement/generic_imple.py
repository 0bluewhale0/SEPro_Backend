'''
Date: 2023-05-23 17:55:05
LastEditors: ShanZhihan
LastEditTime: 2023-05-23 21:44:01
FilePath: \backEnd\software_site\software_app\implement\generic_imple.py
'''
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from software_app.service.jwt_tools import RequestContext

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
            'minLength': 8,
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
        },
        'key': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 32,
            'errmsg': "key 应为字符串(8~32)"
        }
    }
}


def register_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass

def login_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass

def query_time(_: RequestContext, req: HttpRequest) -> JsonResponse:
    pass