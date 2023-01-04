from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import export, exportBySite, exportNew
from .serializers import ExportSerializer

bySite = ["exclusions", "groups", "installed-applications"]
response_get = {
    "message": "use POST request",
    "parameters": [
        "item:mandatory",
        "index:mandatory",
        "pipeline:optional",
        "limit:optional",
        "timedelta:optional",
    ],
    "example": {
        "item": "agents",
        "index": "c1-s1-agents",
        "pipeline": "c1-geo-ip-agent",
    },
}


class ExportViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        if serializer.data["item"] in bySite:
            task = exportBySite.delay(serializer.data)
            result = {"task_id": task.id}
        else:
            task = export.delay(serializer.data)
            result = {"task_id": task.id}
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)


class ExportViewSetDebug(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        if serializer.data["item"] in bySite:
            result = exportBySite(serializer.data)
        else:
            result = export(serializer.data)
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)
