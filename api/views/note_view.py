from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Note
from api.serializers import NoteSerializer


class NoteList(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        notes = Note.objects.all().order_by('-update_time')
        count = notes.count()
        s = NoteSerializer(notes, many=True, fields=('id', 'title', 'insert_time', 'update_time'))
        resp = {
            'count': count,
            'results': s.data
        }
        return Response(resp, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        s = NoteSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, pk, format=None):
        note = Note.objects.get(pk=pk)
        s = NoteSerializer(note)
        return Response(s.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        note = Note.objects.get(pk=pk)
        s = NoteSerializer(note, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
