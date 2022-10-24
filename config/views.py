from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from config.serializers import (
    UserSerializer,
    GroupSerializer,
    SentinelOneSerializer,
    ElasticSerializer,
    FreshServiceSerializer,
    BexioSerializer,
    SharePointSerializer,
    IntervalScheduleSerializer,
    CrontabScheduleSerializer,
    PeriodicTaskSerializer,
)
from config.models import (
    SentinelOneModel,
    ElasticModel,
    FreshServiceModel,
    BexioModel,
    SharePointModel,
)
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("id")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SentinelOneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = SentinelOneModel.objects.all().order_by("id")
    serializer_class = SentinelOneSerializer
    permission_classes = [permissions.IsAuthenticated]


class ElasticViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = ElasticModel.objects.all().order_by("id")
    serializer_class = ElasticSerializer
    permission_classes = [permissions.IsAuthenticated]


class FreshServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = FreshServiceModel.objects.all().order_by("id")
    serializer_class = FreshServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class BexioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = BexioModel.objects.all().order_by("id")
    serializer_class = BexioSerializer
    permission_classes = [permissions.IsAuthenticated]


class SharePointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = SharePointModel.objects.all().order_by("id")
    serializer_class = SharePointSerializer
    permission_classes = [permissions.IsAuthenticated]


class CrontabScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = CrontabSchedule.objects.all().order_by("id")
    serializer_class = CrontabScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = IntervalSchedule.objects.all().order_by("id")
    serializer_class = IntervalScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SentinelOne entries to be viewed or edited.
    """

    queryset = PeriodicTask.objects.all().order_by("id")
    serializer_class = PeriodicTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
