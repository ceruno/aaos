import asyncio
from connectors.freshservice import FreshServiceAPI
from connectors.elastic import ElasticAPI
from config.models import FreshServiceModel, ElasticModel
from celery import shared_task
from cryptography.fernet import Fernet
import os

key = bytes(os.environ.get("ENCRYPTION_KEY"), 'utf-8')
f = Fernet(key)

@shared_task
def export(args):

    fresh_config = FreshServiceModel.objects.all().values()
 
    results = []
    for i in list(fresh_config):

        api_key = (f.decrypt(i['api_key'])).decode()
        fresh_session = FreshServiceAPI(i, api_key, args['item'])
        
        task = asyncio.run(fresh_session.getAll())
        results.extend(task)

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