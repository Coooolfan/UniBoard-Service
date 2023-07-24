from django.urls import path

from api.views.client import report

urlpatterns = [
    path("report/", report.index, name="report"),
]
