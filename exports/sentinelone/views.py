from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import export, exportBySite

bySite = ['exclusions', 'groups','installed-applications']
response_get = {'message': 'use POST request', 
                'parameters': ['item:mandatory', 'index:mandatory', 'pipeline:optional', 'limit:optional', 'timedelta:optional'],
                'example': {'item': 'agents', 'index': 'c1-s1-agents', 'pipeline': 'c1-geo-ip-agent'}}  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main(request):
    if request.method == 'POST':
        if request.data['item'] in bySite:
            task = exportBySite.delay(request.data)
        else:
            task = export.delay(request.data)
        result = task.id
        response_post = {'message': 'task added', 'task_id': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def debug(request):
    if request.method == 'POST':
        if request.data['item'] in bySite:
            result = exportBySite(request.data)
        else:
            result = export(request.data)
        response_post = {'message': 'task executed', 'result': result, 'post': request.data}
        return Response(response_post)
    return Response(response_get)