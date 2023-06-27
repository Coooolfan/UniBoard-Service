from django.urls import path

from api.views.board import note
from api.views.board import report

urlpatterns = [
    path("note/", note.index, name="note"),
    path("report/", report.index, name="report"),
]
