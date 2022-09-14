from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import export

response_get = {'message': 'use POST request', 
                'parameters': ['item:mandatory', 'index:mandatory'],
                'example': {'item': 'tickets', 'index': 'c1-s1-tickets'}}  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main(request):
    if request.method == 'POST':
        task = export.delay(request.data)
        result = task.id
        response_post = {'message': 'task added', 'task_id': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def debug(request):
    if request.method == 'POST':
        result = export(request.data)
        response_post = {'message': 'task executed', 'result': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)