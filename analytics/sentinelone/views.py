from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import licensing

response_get = {'message': 'use POST request'}  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def usage(request):
    if request.method == 'POST':
        task = licensing.delay(request.data)
        result = task.id
        response_post = {'message': 'task added', 'task_id': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def usage_debug(request):
    if request.method == 'POST':
        result = licensing(request.data)
        response_post = {'message': 'task executed', 'result': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)