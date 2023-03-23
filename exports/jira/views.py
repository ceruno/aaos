from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import export
from .serializers import ExportSerializer

response_get = {
    "message": "use POST request",
    "parameters": [
        "item:mandatory",
        "project:mandatory",
        "index:mandatory",
        "pipeline:optional",
    ],
    "example": {"item": "search", "project": "TMPL", "index": "ccsc-jira-issues"},
}


class ExportViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
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
        result = export(serializer.data)
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)
