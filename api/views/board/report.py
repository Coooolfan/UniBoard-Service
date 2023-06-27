import json
from secrets import token_hex

from django.core.cache import cache
from django.http import HttpResponse
from pyotp import TOTP

from uniboard.settings import TwoFA_SecretKey


# Create your views here.
def index(request):
    if request.method == "POST":
        decoded_data = request.body.decode()
        received_data = json.loads(decoded_data)
        key = received_data["key"]
        if check_code(key):
            data = {
                "verified": True,
                "token": create_token(),
            }
            return HttpResponse(json.dumps(data))
        return HttpResponse()
    else:
        return HttpResponse(status=404)


def check_code(key):
    totp = TOTP(TwoFA_SecretKey)
    return totp.verify(key)


def create_token():
    new_token = token_hex(64)
    cache.set("token", new_token)
    return new_token
