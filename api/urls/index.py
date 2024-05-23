from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import sysInfo

urlpatterns = [
    re_path(r'^sysInfo/$', sysInfo.SysInfoList.as_view()),
    re_path(r'^sysInfo/(?P<pk>[0-9]+)$', sysInfo.SysInfoDetaile.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
