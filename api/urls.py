from django.urls import path, include

from . import views, urls

urlpatterns = [
    path("", views.index, name="index"),
    path("board/", include(api.urls.board.index), name="board")
]