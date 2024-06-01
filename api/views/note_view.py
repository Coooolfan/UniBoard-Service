from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Note
from api.serializers import NoteSerializer


class NoteList(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Note.objects.all()
        s = NoteSerializer(queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        s = NoteSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, pk, format=None):
        try:
            sysinfo = Note.objects.get(pk=pk)
            serializer = NoteSerializer(sysinfo)
            return Response(serializer.data)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            sysinfo = Note.objects.get(pk=pk)
            sysinfo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        try:
            sysinfo = Note.objects.get(pk=pk)
            serializer = NoteSerializer(sysinfo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
