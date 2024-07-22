from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *

# schema_view = get_schema_view(
#     openapi.Info(
#         title="UniBoard API",
#         default_version='v1',
#         description="Test description",
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny]
# )

urlpatterns = [
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('token/totp/', TOTPDetail.as_view(), name='totp-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('user-info/', UserInfoList.as_view(), name='user-info-list'),
    path('user-info/<int:pk>/', UserInfoDetail.as_view(), name='user-info-detail'),

    path('sys-config/', SysConfigList.as_view(), name='sys-config-list'),
    path('sys-config/<int:pk>/', SysConfigDetail.as_view(), name='sys-config-detail'),

    path('short-urls/', ShortUrlList.as_view(), name='short-url-list'),
    path('short-urls/<int:pk>/', ShortUrlDetails.as_view(), name='short-url-detail'),

    path('hyperlinks/', HyperLinkList.as_view(), name='hyper-link-list'),
    path('hyperlinks/<int:pk>/', HyperLinkDetail.as_view(), name='hyper-link-detail'),

    path('hyperlink-caches/', HyperLinkCacheList.as_view(), name='hyper-link-cache-list'),
    path('hyperlink-caches/<int:pk>/', HyperLinkCacheDetail.as_view(), name='hyper-link-cache-detail'),

    path('monitored-objects/', MonitoredObjectList.as_view(), name='monitored-object-list'),
    path('monitored-objects/<int:pk>/', MonitoredObjectDetail.as_view(), name='monitored-object-detail'),
    path('monitored-objects/<int:pk>/metrics/', MetricDataDetail.as_view(), name='monitored-object-metrics'),

    path('metrics/', MetricList.as_view(), name='metric-list'),
    path('metrics/<int:pk>/', MetricDetail.as_view(), name='metric-detail'),

    path('object-metrics/', ObjectMetricList.as_view(), name='object-metric-list'),
    path('object-metrics/<int:pk>/', ObjectMetricDetail.as_view(), name='object-metric-detail'),

    path('note/', NoteList.as_view(), name='note-list'),
    path('note/<int:pk>/', NoteDetail.as_view(), name='note-detail'),

    path('file-records/', FileRecordList.as_view(), name='file-record-list'),
    path('file-records/<str:pk>/', FileRecordDetail.as_view(), name='file-record-detail'),

    path('file-records/<int:pk>/token/', FileRecordTokenDetail.as_view(), name='file-record-token-detail'),
]
