from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import update

response_get = {'message': 'use POST request', 
                'parameters': ['item:mandatory'],
                'example': {'item': 'update'}}  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main(request):
    if request.method == 'POST':
        match request.data['item']:
            case 'update':
                task = update.delay(request.data)
                result = 'task_id ' + task.id
            case _:
                result = 'bad parameter'
        response_post = {'message': 'task added', 'result': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def debug(request):
    if request.method == 'POST':
        match request.data['item']:
            case 'update':
                result = update(request.data)
            case _:
                result = 'bad parameter'
        response_post = {'message': 'task executed', 'result': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)