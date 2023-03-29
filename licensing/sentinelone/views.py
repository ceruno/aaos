from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import usage, usage_fresh, expiration, expiration_fresh
from .serializers import ExportSerializer

response_get = {
    "message": "use POST request",
    "parameters": ["item:mandatory", "target:mandatory"],
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
                match serializer.data["target"]:
                    case "jira":
                        task = usage.delay(serializer.data)
                        result = {"task_id": task.id}
                    case "freshservice":
                        task = usage_fresh.delay(serializer.data)
                        result = {"task_id": task.id}
                    case _:
                        result = "bad parameter"
            case "expiration":
                match serializer.data["target"]:
                    case "jira":
                        task = expiration.delay(serializer.data)
                        result = {"task_id": task.id}
                    case "freshservice":
                        task = expiration_fresh.delay(serializer.data)
                        result = {"task_id": task.id}
                    case _:
                        result = "bad parameter"
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
                match serializer.data["target"]:
                    case "jira":
                        result = usage(serializer.data)
                    case "freshservice":
                        result = usage_fresh(serializer.data)
                    case _:
                        result = "bad parameter"
            case "expiration":
                match serializer.data["target"]:
                    case "jira":
                        result = expiration(serializer.data)
                    case "freshservice":
                        result = expiration_fresh(serializer.data)
                    case _:
                        result = "bad parameter"
            case _:
                result = "bad parameter"
        response_post = {
            "message": "task added",
            "result": result,
            "post": request.data,
        }
        return Response(response_post)
