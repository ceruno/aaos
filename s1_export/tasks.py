import asyncio
from readline import append_history_file
from connectors.sentinelone import SentinelOne as S1_Connector
from connectors.elastic import Elastic as Elastic_Connector
from configuration.models import SentinelOne as S1_Model, Elastic as Elastic_Model
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def getAgents():
    s1_config = list(S1_Model.objects.all().values())
    elastic_config = list(Elastic_Model.objects.all().values())
    agents = []
    for i in s1_config:
        token = (f.decrypt(i['token'])).decode()
        s1_session = S1_Connector(i['console_url'], token, 'Agents')
        task = asyncio.run(s1_session.getAgents())
        agents.extend(task)
    for i in elastic_config:
        password = (f.decrypt(i['password'])).decode()
        elastic_session = Elastic_Connector(i['elastic_url'], i['user'], password)
        task = elastic_session.writeAgents(agents)
    return('done')