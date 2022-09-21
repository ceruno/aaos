import asyncio
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from config.models import SentinelOneModel, ElasticModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

# Celery logging version
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

import logging
logger = logging.getLogger('aaos')

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def export(args):

    s1_config = SentinelOneModel.objects.all().values()
    logger.info('getting S1 config')

    results = []
    for config in list(s1_config):

        token = (f.decrypt(config['token'])).decode()
        s1_session = SentinelOneAPI(config['sentinelone_url'], token, args['item'])
        
        if 'timedelta' in args.keys():
            task = asyncio.run(s1_session.getByDelta(args['timedelta']))
        elif ('limit' in args.keys()) and (args['limit'] == 'true'):
            task = asyncio.run(s1_session.get1000())
        else:
            task = asyncio.run(s1_session.getAll())
        results.extend(task)

    return(write(args, results))

@shared_task
def exportBySite(args):

    s1_config = SentinelOneModel.objects.all().values()
    
    sites = []
    results = []
    for config in list(s1_config):

        token = (f.decrypt(config['token'])).decode()
        s1_session = SentinelOneAPI(config['sentinelone_url'], token, 'sites')
        
        task1 = asyncio.run(s1_session.getAll())
        sites.extend(task1)

        for site in sites:
            s1_session = SentinelOneAPI(config['sentinelone_url'], token, args['item'])
            task2 = asyncio.run(s1_session.getBySite(site))
            results.extend(task2)

    return(write(args, results))

def write(args, results):

    elastic_config = ElasticModel.objects.all().values()

    if not 'pipeline' in args.keys():
        args['pipeline'] = None
    
    timestamp = True
    if args['item'] == 'activities':
        timestamp = False
    
    for config in list(elastic_config):
        password = (f.decrypt(config['password'])).decode()
        elastic_session = ElasticAPI(config, password, timestamp, args['index'], args['pipeline'])
        result = elastic_session.write(results)

    return(result)