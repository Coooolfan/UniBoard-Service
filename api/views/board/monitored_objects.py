from django.http import HttpResponse, JsonResponse
import json
from django.core.cache import cache
from api.models import MonitoredObjects
from api.serializers import MonitoredObjectsSerializer as ObjSerializer


def index(request):
    if request.method == "POST":
        return HttpResponse(status=404)
    objs = MonitoredObjects.objects.all()
    serializer = ObjSerializer(objs, many=True)
    data = {"monitored_objects": serializer.data}
    return HttpResponse(json.dumps(data))
