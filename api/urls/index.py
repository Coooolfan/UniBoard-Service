from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import sysInfo

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^sysInfo/$', sysInfo.SysInfoList.as_view()),
    re_path(r'^sysInfo/(?P<pk>[0-9]+)$', sysInfo.SysInfoDetaile.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
