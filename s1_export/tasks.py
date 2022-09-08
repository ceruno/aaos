import asyncio
from connectors.sentinelone import SentinelOne as S1
from configuration.models import SentinelOne as Model
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def getAgents():
    s1_config = list(Model.objects.all().values())
    agents = []
    for i in s1_config:
        token = (f.decrypt(i['token'])).decode()
        session = S1(i['console_url'], token, 'Agents')
        task = asyncio.run(session.getAgentInfo())
        agents.extend(task)
    return(agents)