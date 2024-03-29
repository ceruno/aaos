import asyncio
from connectors.postgres import PostgresAPI
from connectors.elastic import ElasticAPI
from connectors.loki import LokiAPI
from connectors.dataset import DataSetAPI
from config.models import PostgresModel, ElasticModel, LokiModel, DataSetModel
from celery import shared_task
from cryptography.fernet import Fernet
import os


key = bytes(os.environ.get("ENCRYPTION_KEY"), "utf-8")
f = Fernet(key)


@shared_task
def exportMain(args):

    postgres_config = PostgresModel.objects.all().values()

    response = []
    for config in list(postgres_config):

        task = export.delay(args, config)
        response.append(task.id)

    return response


@shared_task
def export(args, config):

    results = []

    password = (f.decrypt(config["password"])).decode()
    postgres_session = PostgresAPI(config, password, args["query"])

    task = asyncio.run(postgres_session.get())
    results.extend(task)

    response = []

    elastic_task = writeElastic.delay(args, results)
    response.append(elastic_task.id)
    loki_task = writeLoki.delay(args, results)
    response.append(loki_task.id)
    dataset_task = writeDataSet.delay(args, results)
    response.append(dataset_task.id)

    return response


@shared_task
def writeElastic(args, results):

    elastic_config = ElasticModel.objects.all().values()

    result = []
    timestamp = True

    if args["item"] == "activities":
        timestamp = False

    for config in list(elastic_config):
        password = (f.decrypt(config["password"])).decode()
        elastic_session = ElasticAPI(
            config, password, timestamp, args["index"], args["pipeline"]
        )
        task = elastic_session.write(results)
        result.append(task)

    return result


@shared_task
def writeLoki(args, results):

    loki_config = LokiModel.objects.all().values()

    result = []

    for config in list(loki_config):
        token = (f.decrypt(config["token"])).decode()
        loki_session = LokiAPI(config, token, "postgres", args["item"])
        task = loki_session.write(results)
        result.append(task)

    return result


@shared_task
def writeDataSet(args, results):

    dataset_config = DataSetModel.objects.all().values()

    result = []

    for config in list(dataset_config):
        token = (f.decrypt(config["token"])).decode()
        dataset_session = DataSetAPI(config, token, "postgres", args["item"])
        task = dataset_session.write(results)
        result.append(task)

    return result
