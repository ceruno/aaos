import asyncio
from readline import append_history_file
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from config.models import SentinelOneModel, ElasticModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def getAgents():
    s1_config = list(SentinelOneModel.objects.all().values())
    elastic_config = list(ElasticModel.objects.all().values())
    agents = []
    for i in s1_config:
        token = (f.decrypt(i['token'])).decode()
        s1_session = SentinelOneAPI(i['console_url'], token, 'Agents')
        task = asyncio.run(s1_session.getAgents())
        agents.extend(task)
    for i in elastic_config:
        password = (f.decrypt(i['password'])).decode()
        elastic_session = ElasticAPI(i['elastic_url'], i['user'], password)
        task = elastic_session.writeAgents(agents)
    return('done')