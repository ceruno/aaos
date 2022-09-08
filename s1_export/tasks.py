from connectors.sentinelone import SentinelOne
import configuration.models
from celery import shared_task

@shared_task
def getUsers():
    s1_config = list(configuration.models.SentinelOne.objects.all())
    session = SentinelOne()