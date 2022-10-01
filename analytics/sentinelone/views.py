from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import update
from .serializers import ExportSerializer

response_get = {'message': 'use POST request', 
                'parameters': ['item:mandatory'],
                'example': {'item': 'update'}}

class ExportViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        match serializer.data['item']:
            case 'update':
                task = update.delay(serializer.data)
                result = {'task_id': task.id}
            case _:
                result = 'bad parameter'
        response_post = {'message': 'task added', 'result': result, 'post': request.data}
        return Response(response_post)

class ExportViewSetDebug(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ExportSerializer

    def list(self, request):
        return Response(response_get)

    def create(self, request):
        serializer = ExportSerializer(request.data)
        match serializer.data['item']:
            case 'update':
                result = update(serializer.data)
            case _:
                result = 'bad parameter'
        response_post = {'message': 'task added', 'result': result, 'post': request.data}
        return Response(response_post)