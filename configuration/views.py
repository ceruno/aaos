from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from configuration.serializers import UserSerializer, GroupSerializer, SentinelOneSerializer, ElasticSerializer, FreshServiceSerializer
from configuration.models import Elastic, FreshService, SentinelOne


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class SentinelOneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """
    queryset = SentinelOne.objects.all()
    serializer_class = SentinelOneSerializer
    permission_classes = [permissions.IsAuthenticated]

class ElasticViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """
    queryset = Elastic.objects.all()
    serializer_class = ElasticSerializer
    permission_classes = [permissions.IsAuthenticated]

class FreshServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """
    queryset = FreshService.objects.all()
    serializer_class = FreshServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
