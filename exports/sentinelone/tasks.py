import asyncio
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from config.models import SentinelOneModel, ElasticModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def export(args):

    s1_config = list(SentinelOneModel.objects.all().values())
    elastic_config = list(ElasticModel.objects.all().values())
    
    results = []
    for i in s1_config:

        token = (f.decrypt(i['token'])).decode()
        s1_session = SentinelOneAPI(i['console_url'], token, args['item'])
        
        task = asyncio.run(s1_session.getAll())
        if 'timedelta' in args.keys():
            task = asyncio.run(s1_session.getDelta(args['timedelta']))
        if ('limit' in args.keys()) and (args['limit'] == 'true'):
            task = asyncio.run(s1_session.get1000())
        results.extend(task)

    if not 'pipeline' in args.keys():
        args['pipeline'] = None
    
    timestamp = True
    if args['item'] == 'activities':
        timestamp = False
    
    for i in elastic_config:
        password = (f.decrypt(i['password'])).decode()
        elastic_session = ElasticAPI(i['elastic_url'], i['user'], password, timestamp, args['index'], args['pipeline'])
        task = elastic_session.write(results)
    
    return('done')

@shared_task
def exportBySite(args):
    
    s1_config = list(SentinelOneModel.objects.all().values())
    elastic_config = list(ElasticModel.objects.all().values())

    sites = []
    results = []
    for i in s1_config:

        token = (f.decrypt(i['token'])).decode()
        s1_session = SentinelOneAPI(i['console_url'], token, 'sites')
        
        task1 = asyncio.run(s1_session.getAll())
        sites.extend(task1)

        for site in sites:
            s1_session = SentinelOneAPI(i['console_url'], token, args['item'])
            task2 = asyncio.run(s1_session.getBySite(site))
            results.extend(task2)

    if not 'pipeline' in args.keys():
        args['pipeline'] = None
    
    timestamp = True
    if args['item'] == 'activities':
        timestamp = False
    
    for i in elastic_config:
        password = (f.decrypt(i['password'])).decode()
        elastic_session = ElasticAPI(i['elastic_url'], i['user'], password, timestamp, args['index'], args['pipeline'])
        task = elastic_session.write(results)

    return('done')