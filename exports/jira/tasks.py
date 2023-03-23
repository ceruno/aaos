import asyncio
from connectors.jira import JiraAPI
from connectors.elastic import ElasticAPI
from config.models import JiraModel, ElasticModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), "utf-8")
f = Fernet(key)


@shared_task
def export(args):

    jira_config = JiraModel.objects.all().values()
    results = []

    for config in list(jira_config):

        token = (f.decrypt(config["token"])).decode()
        jira_session = JiraAPI(config, token, args)
        task = asyncio.run(jira_session.getAll())
        results.extend(task)
        return write(args, results)


def write(args, results):

    elastic_config = ElasticModel.objects.all().values()

    result = []
    timestamp = True

    for config in list(elastic_config):
        password = (f.decrypt(config["password"])).decode()
        elastic_session = ElasticAPI(
            config, password, timestamp, args["index"], args["pipeline"]
        )
        task = elastic_session.write(results)
        result.append(task)

    return result
