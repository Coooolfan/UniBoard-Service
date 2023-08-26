import datetime
import json

from django.http import HttpResponse
from api.models import Status
from api.models import MonitoredObjects


def index(request):
    if request.method != "GET":
        return HttpResponse(status=404)

    # 获取请求的参数
    object_ids = request.GET.getlist("objectIDs[]")
    start_time = request.GET.get("startTime")
    end_time = request.GET.get("endTime")
    items = request.GET.getlist("items[]")
    density = int(request.GET.get("density"))
    last = request.GET.get("last").lower() == "true"
    # 校验ID的合法性
    if not check_ids(object_ids):
        return HttpResponse(json.dumps({"msg": "无效id"}), status=400)

    all_status = []
    for object_id in object_ids:
        status = get_status(object_id, start_time, end_time, items, density, last)
        all_status.append(status)

    # 返回状态列表
    return HttpResponse(json.dumps({"data": all_status}))


def get_status(object_id, start_time, end_time, items: list, density, last) -> dict:
    # 将时间戳转换为datetime对象,时区的设置不影响程序运行，仅避免数据库warning
    start_time = datetime.datetime.fromtimestamp(int(start_time), tz=datetime.timezone.utc)
    end_time = datetime.datetime.fromtimestamp(int(end_time), tz=datetime.timezone.utc)
    # 按时间段查询
    status = Status.objects.filter(objectID=object_id).filter(reportStamp__range=(start_time, end_time))
    # 筛选出时间段内的所有状态
    status = status.values("reportStamp", "status")
    # QuerySet转换为list并预处理datatime对象
    # 并按要求筛选出需要的状态
    list_data = list(status)
    # 如果前端只需要最后一条数据，则只返回最后一条数据
    if last:
        list_data = list_data[-1:]
    formated_status: list = []
    for i in range(len(list_data)):
        reportStamp_int = int(list_data[i]["reportStamp"].timestamp())
        # 字典推导式，筛选出需要的状态
        status_dict = dict({key: list_data[i]["status"][key] for key in items})
        # 将状态列表中的每个状态转换为字典
        formated_status.append({
            "reportTime": reportStamp_int,
            "status": status_dict
        })
    return_data = {
        "objectID": str(object_id),
        "data": formated_status
    }
    # 将状态列表按照density进行筛选
    # status = status[::density]
    return return_data


def check_args(request_json) -> bool:
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
    if "last" not in request_json:
        return False
    return True


def check_ids(object_ids) -> bool:
    exist_ids = MonitoredObjects.objects.values_list("objectID", flat=True)
    exist_ids = list(exist_ids)
    for object_id in object_ids:
        if int(object_id) not in exist_ids:
            return False
    return True
