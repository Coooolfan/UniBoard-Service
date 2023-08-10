from django.http import HttpResponse
import json
from api.models import Status
import datetime

from api.models import MonitoredObjects
from api.apps import get_threshold


def index(request):
    if request.method == "GET":
        return HttpResponse(status=404)

    # 校验终端token
    received_data = json.loads(request.body.decode())
    token = received_data["token"]
    obj_id = received_data["objectID"]
    if not check_token(token, obj_id):
        return HttpResponse(status=201)

    # 从请求体中获取数据
    data: json = received_data["data"]
    report_stamp = received_data["reportStamp"]

    # 保存数据
    save2database(obj_id, data, report_stamp)

    # 更新数据库周期状态
    update_period_status(obj_id, data, report_stamp)

    return HttpResponse(json.dumps({}))


def check_token(token, obj_id):
    # return True
    true_token = MonitoredObjects.objects.filter(objectID=obj_id).values("token")
    # 转换成字符串
    true_token = true_token[0]["token"]
    return token == true_token


def save2database(obj_id, data, report_stamp):
    report_stamp = datetime.datetime.fromtimestamp(int(report_stamp), tz=datetime.timezone(datetime.timedelta(hours=8)))
    Status(
        objectID=obj_id,
        reportStamp=report_stamp,
        status=data
    ).save()


def update_period_status(obj_id, data, report_stamp):
    from api.models import PeriodStatus
    # 获取此对象的最新周期状态
    period_status = PeriodStatus.objects.filter(objectID=obj_id).last()
    # 转换为datetime对象，定义时区为标准UTC
    report_stamp = datetime.datetime.fromtimestamp(int(report_stamp), tz=datetime.timezone.utc)
    # 非空判断
    if period_status is None:
        # 如果没有周期状态，创建一个周期状态
        new_status = {}
        for key, val in data.items():
            check_threshold(obj_id, key, val)
            new_status[key] = get_threshold_count(obj_id, key)
        PeriodStatus(
            objectID=obj_id,
            startStamp=report_stamp,
            endStamp=report_stamp,
            status=new_status
        ).save()
        return
    # 上一个阶段结束，新建周期状态
    if report_stamp - period_status.startStamp > datetime.timedelta(hours=2):
        del_threshold_count(obj_id)
        new_status = {}
        for key, val in data.items():
            check_threshold(obj_id, key, val)
            new_status[key] = get_threshold_count(obj_id, key)
        PeriodStatus(
            objectID=obj_id,
            startStamp=report_stamp,
            endStamp=report_stamp,
            status=new_status
        ).save()
    # 上一个阶段未结束，更新周期状态
    else:
        new_status = {}
        for key, val in data.items():
            check_threshold(obj_id, key, val)
            new_status[key] = get_threshold_count(obj_id, key)
        period_status.status = new_status
        period_status.endStamp = report_stamp
        period_status.save()


def check_threshold(obj_id, key, val):
    from django.core.cache import cache
    val = int(val)
    threshold_max, threshold_min = get_threshold(obj_id, key)
    # 如果没有阈值，直接返回
    if threshold_max is None or threshold_min is None:
        return
    # 如果超过阈值，记录次数
    if not (val > threshold_max or val < threshold_min):
        return
    cache_key = "threshold-" + str(obj_id) + "-" + str(key) + "-count"
    # 自增
    if cache.get(cache_key) is None or cache.get(cache_key) == 0:
        cache.set(cache_key, 1)
    else:
        cache.incr(cache_key)


def get_threshold_count(obj_id, key):
    from django.core.cache import cache
    cache_key = "threshold-" + str(obj_id) + "-" + str(key) + "-count"
    val = cache.get(cache_key)
    if val is None:
        return 0
    return val


def del_threshold_count(obj_id):
    from django.core.cache import cache
    # 删除所有阈值计数，阈值计数的key格式为threshold-obj_id-*-count，*为阈值名
    cache_key = "threshold-" + str(obj_id) + "-*" + "-count"
    cache.delete_pattern(cache_key)
    pass
