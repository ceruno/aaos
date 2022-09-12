import aiohttp
from datetime import datetime
import pytz

class SentinelOneAPI:

    def __init__(self, url, token, reason):

        self.url = url
        self.apitoken = token
        self.headers = {'Authorization': 'ApiToken ' + token}
        self.params = {'limit': '1000'}
        self.reason = reason

    async def get(self, session):

        async with session.get(self.url + self.endpoint, params=self.params) as resp:

            assert resp.status == 200
            goal = await resp.json()
            result = goal['data']
            cursor = goal['pagination']['nextCursor']
            return(result, cursor)

    async def getAgents(self):

        self.endpoint = '/web/api/v2.1/agents'
        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))

        async with aiohttp.ClientSession(headers=self.headers) as session:
            agents = []
            result = await SentinelOneAPI.get(self, session)
            agents.extend(result[0])
            while result[1] != None:
                self.params.update({'cursor': result[1]})
                result = await SentinelOneAPI.get(self, session)
                agents.extend(result[0])
        
        for i in agents:
            values = {
                "@timestamp": self.tstamp,
                "managementConsoleUrl": self.url
            }
            i.update(values)
        
        return(agents)