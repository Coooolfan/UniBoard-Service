from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="UniBoard API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('token/totp/', TOTPDetail.as_view(), name='totp-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('sysInfo/', SysInfoList.as_view(), name='sys-info-list'),
    path('sysInfo/<int:pk>/', SysInfoDetail.as_view(), name='sys-info-detail'),

    path('monitored-objects/', MonitoredObjectList.as_view(), name='monitored-object-list'),
    path('monitored-objects/<int:pk>/', MonitoredObjectDetail.as_view(), name='monitored-object-detail'),
    path('monitored-objects/<int:pk>/metrics/', MetricDataDetail.as_view(), name='monitored-object-metrics'),

    path('metrics/', MetricList.as_view(), name='metric-list'),
    path('metrics/<int:pk>/', MetricDetail.as_view(), name='metric-detail'),

    path('object-metrics/', ObjectMetricList.as_view(), name='object-metric-list'),
    path('object-metrics/<int:pk>/', ObjectMetricDetail.as_view(), name='object-metric-detail'),

    path('note/', NoteList.as_view(), name='note-list'),
    path('note/<int:pk>/', NoteDetail.as_view(), name='note-detail'),

]
