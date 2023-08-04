import datetime
import json

from django.http import HttpResponse
from api.models import Status


def index(request):
    if request.method != "POST":
        return HttpResponse(status=404)

    # 校验请求的参数合法性
    if not check_args(json.loads(request.body.decode())):
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({}))


def get_status(object_id, start_time, end_time, items: list, density):
    # 将时间戳转换为datetime对象
    start_time = convert_timestamp_to_datetime(start_time, "Asia/Shanghai")
    end_time = convert_timestamp_to_datetime(end_time, "Asia/Shanghai")
    # 按时间段查询
    status = Status.objects.filter(objectID=object_id).filter(reportStamp__range=(start_time, end_time))
    # 筛选出时间段内的所有状态
    status = status.values("repotyStamp", "status")
    # QuerySet转换为list并预处理datatime对象
    status = list(status)
    for i in range(len(status)):
        status[i]["repotyStamp"] = int(status[i]["repotyStamp"].timestamp())
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
    if "density" not in request_json:
        return False
    if "timezone" not in request_json:
        return False
    return True


import datetime
import pytz


def convert_timestamp_to_datetime(timestamp_str, timezone_str):
    # 将时间戳字符串转换为整数
    timestamp = int(timestamp_str)

    # 使用 datetime 模块的 fromtimestamp() 方法将时间戳转换为 datetime 对象
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)

    # 获取目标时区对象
    target_timezone = pytz.timezone(timezone_str)

    # 使用目标时区对象的 localize() 方法将 datetime 对象转换为特定时区的时间
    localized_datetime = target_timezone.localize(datetime_obj)

    return localized_datetime
