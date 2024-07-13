import time

from django.contrib.auth.models import User
from django.core.cache import cache
from pyotp import TOTP
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class TOTPDetail(APIView):

    def post(self, request):
        # 还没开发完，先返回400
        return Response(status=400, data={"detail": "Invalid key"})

        keys = cache.keys("totp_*")
        if len(keys) >= 5:
            return Response(status=400, data={"detail": "Too many tries"})
        key = request.data.get("key")
        TOTP_SECRET_KEY = SysConfig.objects.get(pk=1).TOTP_SECRET_KEY
        OTP_code = TOTP(TOTP_SECRET_KEY).now()
        if key != OTP_code:
            # 失败才记录，成功不限制登录次数
            cache.set("totp_" + str(int(time.time())), key, 5 * 60)
            return Response(status=400, data={"detail": "Invalid key"})
        users = User.objects.all()
        if users.count() != 1:
            return Response(status=400, data={"detail": "Invalid user"})
        user = users[0]
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(status=200, data=data)
