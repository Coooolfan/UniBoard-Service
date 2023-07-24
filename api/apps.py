from django.apps import AppConfig
import os
import json
from secrets import token_hex

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

        self.save2database(config_data)

    def save2database(self, config_data):
        from api.models import MonitoredObjects
        for config in config_data:
            MonitoredObjects(
                objectID=config["objectID"],
                objectName=config["objectName"],
                category=config["category"],
                statusList=config["statusList"],
                token=token_hex(16)
            ).save()

