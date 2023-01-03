from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import usage, expiration
from .serializers import ExportSerializer

response_get = {
    "message": "use POST request",
    "parameters": ["item:mandatory"],
    "example": {"item": "usage"},
}


class ExportViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        match serializer.data["item"]:
            case "usage":
                task = usage.delay(serializer.data)
                result = {"task_id": task.id}
            case "expiration":
                task = expiration.delay(serializer.data)
                result = {"task_id": task.id}
            case _:
                result = "bad parameter"
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
        match serializer.data["item"]:
            case "usage":
                result = usage(serializer.data)
            case "expiration":
                result = expiration(serializer.data)
            case _:
                result = "bad parameter"
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)
