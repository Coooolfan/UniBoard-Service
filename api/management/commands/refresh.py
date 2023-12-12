from django.core.management.base import BaseCommand, CommandError
from django.apps import AppConfig
import os
import json
from secrets import token_hex


class Command(BaseCommand):
    help = "update object details in database"

    def add_arguments(self, parser):
        parser.add_argument("obj_names",
                            nargs="*",
                            type=str,
                            help="object names to update, separated by space"
                            )
        parser.add_argument(
            "--all",
            default=False,
            type=bool,
            help="refresh all objects, ignore obj_names",
        )

    def handle(self, *args, **options):
        if options["all"]:
            self.stdout.write("refreshing all objects")
            # load_configs函数在refresh_all为True时无需传入obj_names
            load_configs(True, [])
        elif not len(options["obj_names"]):
            raise CommandError("no object name specified")
        else:
            self.stdout.write("refreshing objects: " + str(options["obj_names"]))
            res: list = load_configs(False, options["obj_names"])
            if len(res):
                self.stdout.write("WARNNING!!!\nobject not found: " + str(res))


def load_configs(refresh_all: bool, obj_names: list):
    # 读取程序根目录下的config.json文件
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    try:
        config_file = os.path.join(BASE_DIR, 'config.json')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        f.close()
    except Exception as e:
        print(e)
        print("config file parse failed, using default config")
        config_file = os.path.join(BASE_DIR, 'config.json.example')
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        f.close()

    for config in config_data:
        # 当指定了要刷新的对象时，只刷新指定的对象，刷新后从列表中删除
        if (config["objectName"] in obj_names) or refresh_all:
            save2database(config)
            if not refresh_all:
                obj_names.remove(config["objectName"])
    return obj_names


def save2database(config):
    from api.models import MonitoredObjects
    token = token_hex(16)
    MonitoredObjects(
        objectID=config["objectID"],
        objectName=config["objectName"],
        category=config["category"],
        statusList=config["statusList"],
        token=token
    ).save()
    print("add monitored object: ", config["objectName"], ", ID: ", config["objectID"], ", token：", token)
