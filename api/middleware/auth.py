
import json
from operator import contains
from secrets import token_hex

from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


def process_request(request: "WSGIRequest"):
    if need_check(request.path):
        if not check_token(request.headers.get("Authorization")):
            print("无效token")
            return HttpResponse(status=201)


# noinspection PyMethodMayBeStatic
def process_response(request: "WSGIRequest", response: "HttpResponse"):
    if need_check(request.path):
        data = json.loads(response.content)
        new_token = create_token()
        data['token'] = new_token
        cache.set("token", new_token)
        response.content = json.dumps(data)
        return response


def check_token(old_token):
    return True
    reality_token = cache.get("token")
    if not old_token == reality_token:
        return True
    else:
        return False


def create_token():
    new_token = token_hex(64)
    return new_token


def need_check(url_path):
    if contains(url_path, "note"):
        return True
    return False


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request:"WSGIRequest"):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response:"HttpResponse" = process_request(request)

        # 当验证中间件有返回内容时，说明校验不通过，直接向客户端返回
        if not response:
            response = self.get_response(request)
            response = process_response(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response
