from django.urls import path

from api.views.board import note
from api.views.board import report
from api.views.board import monitored_objects

urlpatterns = [
    path("note/", note.index, name="note"),
    path("report/", report.index, name="report"),
    path("monitored-objects/", monitored_objects.index, name="monitored-objects"),
]
