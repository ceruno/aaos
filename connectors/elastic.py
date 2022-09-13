from elasticsearch import Elasticsearch, helpers

class ElasticAPI:

    def __init__(self, url, user, password, timestamp, index, pipeline = None):

        self.url = url
        self.user = user
        self.password = password
        self.timestamp = timestamp
        self.index = index
        self.pipeline = pipeline
        self.session = Elasticsearch(self.url, basic_auth=(self.user, self.password))

    def write(self, results):
        
        data = [
            {
                '_op_type': 'create',
                '_index' : self.index,
                '_id' : str(node['id']) + " - " + (node['@timestamp']).strftime("%d.%m.%Y, %H:%M:%S"),
                '_source' : node, 
            }
            for node in results
        ]

        if self.pipeline is not None:
            for item in data:
                values = {
                    'pipeline' : self.pipeline
                }
                item.update(values)

        if self.timestamp == False:
            for item in data:
                values = {
                    '_id' : item['_source']['id']
                }
                item.update(values)
        
        while True:
            try:
                helpers.bulk(self.session,data)
                break
            except Exception:
                return