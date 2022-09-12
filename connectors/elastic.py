from datetime import datetime
from elasticsearch import Elasticsearch, helpers

class ElasticAPI:

    def __init__(self, url, user, password):

        self.url = url
        self.user = user
        self.password = password
        self.session = Elasticsearch(self.url, basic_auth=(self.user, self.password))

    def writeAgents(self, agents):

        data = [
            {
                '_op_type': 'create',
                '_index' : 'c1-s1-agents',
                '_id' : node['id'] + " - " + (node['@timestamp']).strftime("%d.%m.%Y, %H:%M:%S"),
                '_source' : node,
                'pipeline' : "c1-geo-ip-agent" 
            }
            for node in agents
        ]

        helpers.bulk(self.session,data)