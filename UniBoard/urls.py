"""
URL configuration for UniBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from UniBoard.settings import DEBUG
from api.views import FileRecordRedirect
from api.views.redirect_view import redirect_view

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
                  path('s/<str:short_code>/', redirect_view, name='redirect_view'),
                  path("api/", include("api.urls.index")),
                  path("file/<str:pk>/<path:filename>", FileRecordRedirect.as_view(),
                       name="file_redirect_view"),
                  path("file/<str:pk>/", FileRecordRedirect.as_view(), name="file_redirect_view"),
              ] + static("media/", document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path("admin/", admin.site.urls),
    ]
