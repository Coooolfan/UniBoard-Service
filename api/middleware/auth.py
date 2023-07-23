import json
from operator import contains
from secrets import token_hex

from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


def process_request(request: "WSGIRequest"):
    if need_check(request.path):
        token_sent = request.headers.get("Authorization")[7:]
        device_id = request.headers.get("deviceID")
        if not check_token(token_sent, device_id):
            print("无效token")
            return HttpResponse(status=201)


# noinspection PyMethodMayBeStatic
def process_response(request: "WSGIRequest", response: "HttpResponse"):
    if need_check(request.path) and response.status_code == 200:
        data = json.loads(response.content)
        data["token"] = set_new_token(request.headers.get("deviceID"))
        response.content = json.dumps(data)
        return response
    return response


def check_token(old_token, device_id):
    reality_token = cache.get("token-" + device_id)
    if old_token == reality_token:
        return True
    else:
        return False


def set_new_token(decive_id):
    time_expired = cache.ttl("token-" + decive_id)
    if time_expired < 60:
        new_token = token_hex(64)
        cache.set("token-" + decive_id, new_token, timeout=60 * 5)
    else:
        new_token = cache.get("token-" + decive_id)
    return new_token


def need_check(url_path):
    if contains(url_path, "note") or contains(url_path, "monitored-objects"):
        return True
    return False


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: "WSGIRequest"):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response: "HttpResponse" = process_request(request)

        # 当验证中间件有返回内容时，说明校验不通过，直接向客户端返回
        if not response:
            response = self.get_response(request)
            response = process_response(request, response)

        # Code to be executed for each request/response after
        # the view is called.

        return response
