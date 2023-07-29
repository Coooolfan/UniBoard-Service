import json

from django.http import HttpResponse
from api.models import Status


def index(request):
    if request.method != "POST":
        return HttpResponse(status=404)

    if not check_args(json.loads(request.body.decode())):
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({}))


def get_status(object_id, start_time, end_time, items):
    pass

def check_args(request_json):
    if "startTime" not in request_json:
        return False
    if "endTime" not in request_json:
        return False
    if "items" not in request_json or len(request_json["items"]) == 0:
        return False
    if "objectIDs" not in request_json or len(request_json["objectIDs"]) == 0:
        return False
    return True
