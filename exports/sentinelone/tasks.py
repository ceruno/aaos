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

    s1_config = SentinelOneModel.objects.all().values()
 
    results = []
    for i in list(s1_config):

        token = (f.decrypt(i['token'])).decode()
        s1_session = SentinelOneAPI(i['console_url'], token, args['item'])
        
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
    for i in list(s1_config):

        token = (f.decrypt(i['token'])).decode()
        s1_session = SentinelOneAPI(i['console_url'], token, 'sites')
        
        task1 = asyncio.run(s1_session.getAll())
        sites.extend(task1)

        for site in sites:
            s1_session = SentinelOneAPI(i['console_url'], token, args['item'])
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
    
    for i in list(elastic_config):
        password = (f.decrypt(i['password'])).decode()
        elastic_session = ElasticAPI(i['elastic_url'], i['user'], password, timestamp, args['index'], args['pipeline'])
        result = elastic_session.write(results)

    return(result)