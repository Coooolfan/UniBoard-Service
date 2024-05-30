from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import MonitoredObject
from api.serializers import MonitoredObjectSerializer


class MonitoredObjectList(APIView):
    queryset = MonitoredObject.objects.all()
    serializer_class = MonitoredObjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        monitored_objects = MonitoredObject.objects.all()
        serializer = MonitoredObjectSerializer(monitored_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MonitoredObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitoredObjectDetail(APIView):
    queryset = MonitoredObject.objects.all()
    serializer_class = MonitoredObjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return MonitoredObject.objects.get(pk=pk)
        except MonitoredObject.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        monitored_object = self.get_object(pk)
        if monitored_object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MonitoredObjectSerializer(monitored_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        monitored_object = self.get_object(pk)
        if monitored_object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MonitoredObjectSerializer(monitored_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        monitored_object = self.get_object(pk)
        if monitored_object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        monitored_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
