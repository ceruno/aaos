from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import export, exportBySite

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main(request):
    if request.method == 'POST':
        task = export(request.data)
        result = task.id
        response = {'message': 'Task added', 'task_id': result, 'post': request.data}
        return Response(response)
    response = {'message': 'use POST request', 
                'parameters': ['item:mandatory', 'index:mandatory', 'pipeline:optional', 'limit:optional', 'timedelta:optional'],
                'example': {'item': 'agents', 'index': 'c1-s1-agents', 'pipeline': 'c1-geo-ip-agent'}}
    return Response(response)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bySite(request):
    if request.method == 'POST':
        task = exportBySite(request.data)
        result = task.id
        response = {'message': 'Task added', 'task_id': result, 'post': request.data}
        return Response(response)
    response = {'message': 'use POST request', 
                'parameters': ['item:mandatory', 'index:mandatory', 'pipeline:optional', 'limit:optional', 'timedelta:optional'],
                'example': {'item': 'agents', 'index': 'c1-s1-agents', 'pipeline': 'c1-geo-ip-agent'}}
    return Response(response)