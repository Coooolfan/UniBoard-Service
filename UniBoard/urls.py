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

from api.views.redirect_view import redirect_view

urlpatterns = [
                  path('s/<str:short_code>/', redirect_view, name='redirect_view'),
                  path("api/", include("api.urls.index")),
                  path("admin/", admin.site.urls),
              ] + static("media/", document_root=settings.MEDIA_ROOT)
