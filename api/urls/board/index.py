from django.urls import path, include
from api.views.board import note

urlpatterns = [
    path("note/", note.index, name="note"),
]