from rest_framework import permissions
from rest_framework.views import APIView

from api.models import Note
from api.serializers import NoteSerializer


class NoteList(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class NoteDetail(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass
