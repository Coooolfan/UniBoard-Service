import json

from django.http import HttpResponse
from pyotp import TOTP

from api.middleware.auth import set_new_token
from uniboard.settings import TwoFA_SecretKey


# Create your views here.
def index(request):
    if request.method == "POST":
        received_data = json.loads(request.body.decode())
        key = received_data["key"]
        device_id = request.headers.get("deviceID")
        if is_trusted_device(device_id):
            data = {
                "verified": True,
                "token": set_new_token(device_id),
            }
            return HttpResponse(json.dumps(data))

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


def is_trusted_device(device_id):
    from api.models import TrustedDevice
    # # 向数据库中写入数据
    # TrustedDevice(deviceID=device_id).save()
    # return False
    trusted_devices = list(TrustedDevice.objects.values_list("deviceID", flat=True))
    return device_id in trusted_devices
