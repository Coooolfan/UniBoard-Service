from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *
from api.views.note_file_view import NoteFileList

urlpatterns = [
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

    path('note/', NoteList.as_view(), name='note-list'),
    path('note/<int:pk>/', NoteDetail.as_view(), name='note-detail'),

    path('note-files/', NoteFileList.as_view(), name='note-file-list'),

    path('file-records/', FileRecordList.as_view(), name='file-record-list'),
    path('file-records/<str:pk>/', FileRecordDetail.as_view(), name='file-record-detail'),

    path('file-records/<int:pk>/token/', FileRecordTokenDetail.as_view(), name='file-record-token-detail'),
]
