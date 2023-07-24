from django.http import HttpResponse
import json
from api.models import Status
import datetime

from api.models import MonitoredObjects


def index(request):
    if request.method == "GET":
        return HttpResponse(status=404)

    # 校验终端token
    received_data = json.loads(request.body.decode())
    token = received_data["token"]
    obj_id = received_data["objectID"]
    if not check_token(token, obj_id):
        return HttpResponse(status=201)

    data = received_data["data"]
    report_stamp = received_data["reportStamp"]

    # 保存数据
    save2database(obj_id, data, report_stamp)
    return HttpResponse(json.dumps({}))


def check_token(token, obj_id):
    # return True
    true_token = MonitoredObjects.objects.filter(objectID=obj_id).values("token")
    print(true_token)
    print(token)
    return token == true_token


def save2database(obj_id, data, report_stamp):
    report_stamp = datetime.datetime.fromtimestamp(int(report_stamp), tz=datetime.timezone(datetime.timedelta(hours=8)))
    Status(
        objectID=obj_id,
        repotyStamp=report_stamp,
        status=data
    ).save()
