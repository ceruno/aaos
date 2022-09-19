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
    groups = []

    for config in list(fresh_config):

        api_key = (f.decrypt(config['api_key'])).decode()

        fresh_session = FreshServiceAPI(config, api_key, 'groups')
        task1 = asyncio.run(fresh_session.getAll())
        groups.extend(task1)

        if args['item'] != 'groups':
            fresh_session = FreshServiceAPI(config, api_key, args['item'])
            task2 = asyncio.run(fresh_session.getAll(groups))
            results.extend(task2)

    if args['item'] == 'groups':
            return(write(args, groups))
    else:
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