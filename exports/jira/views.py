from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import exportMain
from .serializers import ExportSerializer

response_get = {
    "message": "use POST request",
    "parameters": [
        "item:mandatory",
        "jql:oneof",
        "project:oneof",
        "index:mandatory",
        "pipeline:optional",
    ],
    "example": {
        "item": "table",
        "jql": "status != closed",
        "index": "xyz",
    },
}


class ExportViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        result = exportMain(serializer.data)
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)
