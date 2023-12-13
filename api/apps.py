import json
import os

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            config_file = os.path.join(BASE_DIR, 'config.json')
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            f.close()
        except Exception as e:
            print(e)
            print("配置文件解析失败，使用默认配置")
            config_file = os.path.join(BASE_DIR, 'config.json.example')
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            f.close()
        cache_threshold(config_data)


def cache_threshold(config_data):
    from django.core.cache import cache
    # 对每个对象处理
    for config in config_data:
        # 对每个对象的每个状态处理
        for item in config["statusList"]:
            # 如果没有阈值，跳过
            if not item["threshold"]:
                continue
            # 设置阈值
            key = "threshold-" + str(config["objectID"]) + "-" + item["statusName"]
            cache.set(key + "-max", item["max"])
            cache.set(key + "-min", item["min"])


def get_threshold(obj_id, item):
    from django.core.cache import cache
    key = "threshold-" + str(obj_id) + "-" + item
    threshold_max = cache.get(key + "-max")
    threshold_min = cache.get(key + "-min")
    return threshold_max, threshold_min
