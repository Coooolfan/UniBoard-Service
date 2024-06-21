from django.contrib.auth.models import User
from pyotp import TOTP
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from UniBoard.settings import TOTP_SECRET_KEY


class TOTPDetail(APIView):

    def post(self, request):
        key = request.data.get("key")
        OTP_code = TOTP(TOTP_SECRET_KEY).now()
        if key != OTP_code:
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
