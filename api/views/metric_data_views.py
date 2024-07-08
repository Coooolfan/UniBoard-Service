from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import MetricData
from api.serializers import MetricDataSerializer


class MetricDataDetail(APIView):
    queryset = MetricData.objects.all()
    serializer_class = MetricDataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_metric_by_object(self, object_id):
        try:
            return self.queryset.filter(monitor_object_id=object_id)
        except MetricData.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        metric_data = self.get_metric_by_object(pk)
        if metric_data is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MetricDataSerializer(metric_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
