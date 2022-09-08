from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import getUsers

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def agents(request):
    if request.method == 'POST':
        task = getUsers()
        result = task.id
        spapi = {'message': 'Task added', 'task_id': result, 'post': request.data}
        return Response(spapi)
    spapi = {'message': 'Use POST request', 'test': True}
    return Response(spapi)