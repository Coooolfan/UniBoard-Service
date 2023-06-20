from django.urls import path, include
from api.urls import board

urlpatterns = [
    path("board/", include("api.urls.board.index"), name="board"),
]