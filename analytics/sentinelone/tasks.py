import asyncio
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from connectors.freshservice import FreshServiceAPI
from config.models import SentinelOneModel, ElasticModel, FreshServiceModel
from celery import shared_task
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
import re

key = bytes(os.environ.get('ENCRYPTION_KEY'), 'utf-8')
f = Fernet(key)

@shared_task
def update(args):

    s1_config = SentinelOneModel.objects.all().values()
    fresh_config = FreshServiceModel.objects.all().values()

    activities = []
    tickets = []

    for config in list(s1_config):

        token = (f.decrypt(config['token'])).decode()
        s1_session = SentinelOneAPI(config['sentinelone_url'], token, 'activities')
        activities_single = asyncio.run(s1_session.getByActivityId('5,43'))
        activities.extend(activities_single)

    for config in list(fresh_config):

        api_key = (f.decrypt(config['api_key'])).decode()
        fresh_session = FreshServiceAPI(config, api_key, 'groups')
        groups = asyncio.run(fresh_session.getAll())

        fresh_session = FreshServiceAPI(config, api_key, 'tickets')
        tickets_single = asyncio.run(fresh_session.getAll(groups))
        tickets.extend(tickets_single)

    for config in list(fresh_config):
        
        fresh_session = FreshServiceAPI(config, api_key, 'tickets')
        sent = list(filter(lambda i: re.search('^Software\ update\ availability\ notification\ was\ sent\ to\ (.*)\ by\ (.*)\.', i['primaryDescription']), activities))
        successful = list(filter(lambda i: re.search('^Agent\ (.*)\ was\ successfully\ updated\ to\ version\ (.*)\.', i['primaryDescription']), activities))

        for sent_single in sent:      
            if sent_single['@timestamp'] <= (datetime.now() - timedelta(minutes=60)):
                agent_sent = re.findall('^Software\ update\ availability\ notification\ was\ sent\ to\ (.*)\ by\ .*\.', sent_single['primaryDescription'])
                match = False
                subject = 'SentinelOne: Agent Update Alert - ' + str(agent_sent[0])
                description =   'SentinelOne: Agent Update Alert<br>'\
                                'No successful update after initiation within 60 minutes<br>'\
                                'Management Console URL: ' + sent_single['managementConsoleUrl'] + '<br>'\
                                'Account: ' + sent_single['accountName'] + '<br>'\
                                'Site: ' + sent_single['siteName'] + '<br>'\
                                'Endpoint: ' + agent_sent[0] + '<br>'\
                                'Update initiated: ' + sent_single['@timestamp'].strftime('%d.%m.%Y, %H:%M:%S') + ' UTC'
                tags = ['SentinelOne', 'Agent Update']
                payload = asyncio.run(fresh_session.createPayload(subject, description, tags))         
                for successful_single in successful:
                    agent_successful = re.findall('^Agent\ (.*)\ was\ successfully\ updated\ to\ version\ .*\.', successful_single['primaryDescription'])
                    if agent_sent == agent_successful:
                        timediff = successful_single['@timestamp'] - sent_single['@timestamp']
                        if 0 < timediff.total_seconds() <= 3600:
                            # print(agent_successful[0] + ': ' + sent_single['@timestamp'].strftime('%d.%m.%Y, %H:%M:%S') + ' - ' + successful_single['@timestamp'].strftime('%d.%m.%Y, %H:%M:%S') + ' - ' + str(timediff.total_seconds()))
                            match = True
                if match == False:
                    existing_ticket = checkTicket(tickets, payload)
                    if existing_ticket:
                        initiated = re.findall('Update\ initiated:\ (.*)\ UTC', existing_ticket['description'])[0]
                        if initiated != sent_single['@timestamp'].strftime('%d.%m.%Y, %H:%M:%S'):
                            # asyncio.run(fresh_session.putTicket(existing_ticket['id'], payload))
                            print('Update Ticket for Agent: ' + agent_sent[0])
                        else:
                            print('Ticket: ' + str(existing_ticket['subject']) + ' - existing and up-to-date')
                    else:
                        # asyncio.run(fresh_session.postTicket(payload))
                        print('Create Ticket for Agent: ' + agent_sent[0])

def checkTicket(tickets, payload):
    for ticket in tickets:
        if ticket['subject'] == payload['subject']:
            return(ticket)
    return