from django.core.management.base import BaseCommand

from api.models import UserInfo, SysConfig


class Command(BaseCommand):
    help = "Populate data, 填充默认数据，如系统设置、用户基本信息等，不会覆盖已有数据"

    def handle(self, *args, **options):
        # 创建系统设置
        if SysConfig.objects.count() == 0:
            SysConfig.objects.create()
            self.stdout.write("Created system config")

        # 创建用户基本信息
        if UserInfo.objects.count() == 0:
            UserInfo.objects.get_or_create(
                name="Zhang San",
                name_font="",
                profile="""Programmer, Designer, Writer""",
                contacts={
                    "qq": "",
                    "email": "",
                    "weibo": "",
                    "zhihu": "",
                    "github": "https://github.com/Coooolfan/uniboard",
                    "twitter": "https://twitter.com/",
                    "facebook": "",
                    "linkedin": "",
                    "telegram": "https://t.me/",
                    "instagram": "",
                },
                slogan="Hi, Good Luck Every Day!",
                avatar="avatars/jonas-leupe-QA0pL9yfxk0-avatar.avif",
                banner="banners/paul-pastourmatzis-kN_v2HFm7Tw-banner.avif",
            )
            self.stdout.write("Created user info")
        self.stdout.write("Populated data successfully")
