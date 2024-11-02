from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class TokenChangeDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        req_data: dict = request.data
        old_password = req_data.get("old")
        new_password = req_data.get("new")
        user = request.user
        if not user.check_password(old_password):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid old password"})
        try:
            password_validation.validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK, data={"detail": "Password changed"})
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": e.messages})
