"""JWT工具箱"""
import functools

from enum import Enum
from typing import Callable

from jwt import encode, decode, DecodeError
from django.http import HttpRequest, JsonResponse

from software_app.implement.util.resp_tool import RetCode
from software_app.config import CONFIG

class Role(Enum):
    USER = 0
    ADMIN = 1


class RequestContext:
    def __init__(self, username: str, role: Role) -> None:
        self.username = username
        self.role = role


def gen_token(username: str, role: str) -> str:
    payload = {
        'username': username,
        'role': role
    }
    token = encode(payload, CONFIG['JWT']['secret'], algorithm=CONFIG['JWT']['algorithm'])
    # return token.decode('utf-8')
    return token


# 鉴权
def preprocess_token(
        limited_role: Role
) -> Callable:
    def decorator(request_handler: Callable[[RequestContext, HttpRequest], JsonResponse]):
        @functools.wraps(request_handler)
        def wrapper(request: HttpRequest):
            token: str = request.META.get('HTTP_AUTHORIZATION')
            if token is None:
                return JsonResponse({
                    'code': RetCode.FAIL.value,
                    'message': '需要登录'
                })
            try:
                token = token.removeprefix('Bearer ')
                payload = decode(token, CONFIG['JWT']['secret'], algorithms=['HS256'])
            except DecodeError:
                return JsonResponse({
                    'code': RetCode.FAIL.value,
                    'message': 'JWT损坏'
                })
            username = payload['username']
            role = Role[payload['role']]
            if role != limited_role:
                return JsonResponse({
                    'code': RetCode.FAIL.value,
                    'message': '无权限'
                })
            context = RequestContext(username, role)
            response: JsonResponse = request_handler(context, request)
            return response

        return wrapper

    return decorator
