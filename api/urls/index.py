from django.urls import path

from api.views.sysInfo import index as sysInfo
urlpatterns = [
    path("index.php",sysInfo, name="sysInfo"),
]