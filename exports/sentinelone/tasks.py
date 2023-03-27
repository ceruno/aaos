import asyncio
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from connectors.loki import LokiAPI
from connectors.dataset import DataSetAPI
from config.models import SentinelOneModel, ElasticModel, LokiModel, DataSetModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

# Celery logging version
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

import logging

logger = logging.getLogger("aaos")

bySite = ["exclusions", "groups", "installed-applications"]
key = bytes(os.environ.get("ENCRYPTION_KEY"), "utf-8")
f = Fernet(key)


@shared_task
def exportOld(args):

    s1_config = SentinelOneModel.objects.all().values()
    logger.info("getting S1 config")

    results = []
    for config in list(s1_config):

        token = (f.decrypt(config["token"])).decode()
        s1_session = SentinelOneAPI(config["sentinelone_url"], token, args["item"])

        if args["timedelta"] != "":
            task = asyncio.run(s1_session.getByDelta(args["timedelta"]))
        elif args["limit"] == "true":
            task = asyncio.run(s1_session.get1000())
        else:
            task = asyncio.run(s1_session.getAll())
        results.extend(task)

    response = []

    response.extend(writeElastic(args, results))
    response.extend(writeLoki(args, results))
    response.extend(writeDataSet(args, results))

    return response


@shared_task
def exportMain(args):

    s1_config = SentinelOneModel.objects.all().values()
    logger.info("getting S1 config")

    response = []
    for config in list(s1_config):

        if args["item"] in bySite:

            task = exportBySite.delay(args, config)
            response.append(task.id)

        else:

            task = exportByUrl.delay(args, config)
            response.append(task.id)

    return response


@shared_task
def exportBySite(args, config):

    sites = []
    results = []

    token = (f.decrypt(config["token"])).decode()
    s1_session = SentinelOneAPI(config["sentinelone_url"], token, "sites")

    task1 = asyncio.run(s1_session.getAll())
    sites.extend(task1)

    for site in sites:
        s1_session = SentinelOneAPI(config["sentinelone_url"], token, args["item"])
        task2 = asyncio.run(s1_session.getBySite(site))
        results.extend(task2)

    response = []

    elastic_task = writeElastic.delay(args, results)
    response.append(elastic_task.id)
    loki_task = writeLoki.delay(args, results)
    response.append(loki_task.id)
    dataset_task = writeDataSet.delay(args, results)
    response.append(dataset_task.id)

    return response


@shared_task
def exportByUrl(args, config):

    results = []

    token = (f.decrypt(config["token"])).decode()
    s1_session = SentinelOneAPI(config["sentinelone_url"], token, args["item"])

    if args["timedelta"] != "":
        task = asyncio.run(s1_session.getByDelta(args["timedelta"]))
    elif args["limit"] == "true":
        task = asyncio.run(s1_session.get1000())
    else:
        task = asyncio.run(s1_session.getAll())
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
        loki_session = LokiAPI(config, token, "sentinelone", args["item"])
        task = loki_session.write(results)
        result.append(task)

    return result


@shared_task
def writeDataSet(args, results):

    dataset_config = DataSetModel.objects.all().values()

    result = []

    for config in list(dataset_config):
        token = (f.decrypt(config["token"])).decode()
        dataset_session = DataSetAPI(config, token, "sentinelone", args["item"])
        task = dataset_session.write(results)
        result.append(task)

    return result
