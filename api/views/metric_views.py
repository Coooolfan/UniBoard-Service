from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Metric
from api.serializers import MetricSerializer


class MetricList(APIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        metrics = Metric.objects.all()
        serializer = MetricSerializer(metrics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricDetail(APIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Metric.objects.get(pk=pk)
        except Metric.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        metric = self.get_object(pk)
        if metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MetricSerializer(metric)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        metric = self.get_object(pk)
        if metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MetricSerializer(metric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        metric = self.get_object(pk)
        if metric is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        metric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
