from django.urls import path, include

urlpatterns = [
    path("board/", include("api.urls.board.index"), name="board"),
    path("client/", include("api.urls.client.index"), name="client"),
]