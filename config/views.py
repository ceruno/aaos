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
    LokiSerializer,
    DataSetSerializer,
    PostgresSerializer,
    JiraSerializer,
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
    LokiModel,
    DataSetModel,
    PostgresModel,
    JiraModel,
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
    API endpoint that allows Elastic entries to be viewed or edited.
    """

    queryset = ElasticModel.objects.all().order_by("id")
    serializer_class = ElasticSerializer
    permission_classes = [permissions.IsAuthenticated]


class FreshServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FreshService entries to be viewed or edited.
    """

    queryset = FreshServiceModel.objects.all().order_by("id")
    serializer_class = FreshServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class BexioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Bexio entries to be viewed or edited.
    """

    queryset = BexioModel.objects.all().order_by("id")
    serializer_class = BexioSerializer
    permission_classes = [permissions.IsAuthenticated]


class SharePointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SharePoint entries to be viewed or edited.
    """

    queryset = SharePointModel.objects.all().order_by("id")
    serializer_class = SharePointSerializer
    permission_classes = [permissions.IsAuthenticated]


class LokiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Loki entries to be viewed or edited.
    """

    queryset = LokiModel.objects.all().order_by("id")
    serializer_class = LokiSerializer
    permission_classes = [permissions.IsAuthenticated]


class DataSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows DataSet entries to be viewed or edited.
    """

    queryset = DataSetModel.objects.all().order_by("id")
    serializer_class = DataSetSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostgresViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Postgres entries to be viewed or edited.
    """

    queryset = PostgresModel.objects.all().order_by("id")
    serializer_class = PostgresSerializer
    permission_classes = [permissions.IsAuthenticated]


class JiraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jira entries to be viewed or edited.
    """

    queryset = JiraModel.objects.all().order_by("id")
    serializer_class = JiraSerializer
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
