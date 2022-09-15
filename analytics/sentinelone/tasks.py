import asyncio
from connectors.sentinelone import SentinelOneAPI
from connectors.elastic import ElasticAPI
from connectors.freshservice import FreshServiceAPI
from config.models import SentinelOneModel, ElasticModel, FreshServiceModel
from celery import shared_task
from cryptography.fernet import Fernet
import math
import os
import re

key = bytes(os.environ.get('ENCRYPTION_KEY'), 'utf-8')
f = Fernet(key)

@shared_task
def licensing(args):

    s1_config = SentinelOneModel.objects.all().values()
    fresh_config = FreshServiceModel.objects.all().values()
 
    accounts = []
    sites = []
    tickets = []

    for config in list(s1_config):

        token = (f.decrypt(config['token'])).decode()
        s1_session = SentinelOneAPI(config['console_url'], token, 'accounts')
        accounts_single = asyncio.run(s1_session.getAll())
        accounts.extend(accounts_single)
        s1_session = SentinelOneAPI(config['console_url'], token, 'sites')
        sites_single = asyncio.run(s1_session.getAll())
        sites.extend(sites_single)

    for config in list(fresh_config):

        api_key = (f.decrypt(config['api_key'])).decode()
        fresh_session = FreshServiceAPI(config, api_key, 'groups')
        groups = asyncio.run(fresh_session.getAll())

        fresh_session = FreshServiceAPI(config, api_key, 'tickets')
        tickets_single = asyncio.run(fresh_session.getAll(groups))
        tickets.extend(tickets_single)

    for config in list(fresh_config):
        
        fresh_session = FreshServiceAPI(config, api_key, 'tickets')

        for account in accounts:
            
            if account['totalLicenses'] == 0:
                usageLicenses = 0
            else:
                usageLicenses = math.trunc(account['activeAgents'] / account['totalLicenses'])
            usageLicensesDifference = math.trunc(account['activeAgents'] - account['totalLicenses'])
            
            if  (account['state'] == 'active') and \
                ((usageLicenses >= 1.05 and \
                  usageLicensesDifference >= 10) or \
                 (usageLicensesDifference >= 100)):
                subject = 'SentinelOne: Account Usage Alert - ' + account['name']
                description =   'SentinelOne: Licensing Alert <br>'\
                                'Management Console URL: ' + account['managementConsoleUrl'] + '<br>'\
                                'Account: ' + account['name'] + '<br>'\
                                'Usage: ' + str(usageLicenses * 100) + ' %<br>'\
                                'Licensed: ' + str(account['totalLicenses']) + '<br>'\
                                'Overprovisioned: ' + str(usageLicensesDifference)
                tags = ['SentinelOne', 'Licensing']
                payload = asyncio.run(fresh_session.createPayload(subject, description, tags))
                existing_ticket = checkTicket(tickets, payload)
                if existing_ticket:
                    overprovisioned = re.findall('Overprovisioned:\ (\d*)', existing_ticket['description'])[0]
                    if int(overprovisioned) != usageLicensesDifference:
                        asyncio.run(fresh_session.postTicket(payload, existing_ticket['id']))
                else:
                    asyncio.run(fresh_session.postTicket(payload))

        for site in sites:

            if site['totalLicenses'] == 0:
                usageLicenses = 0
            else:
                usageLicenses = math.trunc(site['activeLicenses'] / site['totalLicenses'])
            usageLicensesDifference = math.trunc(site['activeLicenses'] - site['totalLicenses'])

            if  (site['state'] == 'active') and \
                ((usageLicenses >= 1.05 and \
                  usageLicensesDifference >= 10) or \
                 (usageLicensesDifference >= 100)):
                subject = 'SentinelOne: Site Usage Alert - ' + site['accountName'] + ' - ' + site['name']
                description =   'SentinelOne: Licensing Alert <br>'\
                                'Management Console URL: ' + site['managementConsoleUrl'] + '<br>'\
                                'Account: ' + site['accountName'] + '<br>'\
                                'Site: ' + site['name'] + '<br>'\
                                'Usage: ' + str(usageLicensesDifference * 100) + ' %<br>'\
                                'Licensed: ' + str(site['totalLicenses']) + '<br>'\
                                'Overprovisioned: ' + str(usageLicensesDifference)
                tags = ['SentinelOne', 'Licensing']
                payload = asyncio.run(fresh_session.createPayload(subject, description, tags))
                existing_ticket = checkTicket(tickets, payload)
                if existing_ticket:
                    overprovisioned = re.findall('Overprovisioned:\ (\d*)', existing_ticket['description'])[0]
                    if int(overprovisioned) != usageLicensesDifference:
                        asyncio.run(fresh_session.postTicket(payload, existing_ticket['id']))
                else:
                    asyncio.run(fresh_session.postTicket(payload))

def checkTicket(tickets, payload):
    for ticket in tickets:
        if ticket['subject'] == payload['subject']:
            return(ticket)
    return