import json

from django.http import HttpResponse
from pyotp import TOTP

from api.middleware.auth import set_new_token
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
                "token": set_new_token(request.headers.get("deviceID")),
            }
            return HttpResponse(json.dumps(data))
        return HttpResponse()
    else:
        return HttpResponse(status=404)


def check_code(key):
    totp = TOTP(TwoFA_SecretKey)
    return totp.verify(key)
