import aiohttp
import base64
import math
import pytz
from datetime import datetime

class FreshServiceAPI:

    def __init__(self, config, api_key, item):
        
        self.url = config["service_url"]
        self.api_key = api_key
        self.item = item
        self.endpoint = '/api/v2/' + item
        self.params = {'per_page': '100'}
        self.gid = config["group_id"]
        self.id = config["requester_id"] 
        self.email = config["requester_email"]
        self.phone = config["requester_phone"]
        self.ansprechperson = config["ansprechperson"]

    async def get(self, session):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))

        async with session.get(self.url + self.endpoint, params=self.params) as resp:

            assert resp.status == 200
            goal = await resp.json()
            result = goal[self.item]
            link = resp.links.get('next')

            for i in result:
                values = {
                    "@timestamp": self.tstamp,
                }
                i.update(values)

            return(result, link)

    async def getAll(self):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        results = []
        page = 1

        async with aiohttp.ClientSession(auth = aiohttp.BasicAuth(self.api_key, 'X')) as session:
            result = await self.get(session)
            results.extend(result[0])

            while result[1] != None:
                page += 1
                self.params.update({'page': page})
                result = await self.get(session)
                results.extend(result[0])
        
        return(results)

    # def getGroups(self):
    #     print("Getting Groups from " + self.portal)
    #     s = requests.Session()
    #     basic = HTTPBasicAuth(self.api_key, ":X")
    #     r = s.get(self.portal + "/api/v2/groups", auth = basic)
    #     w = vars(r)["_content"]
    #     encoding = "utf-8"
    #     p = str(w, encoding)
    #     res = json.loads(p)
    #     goal = res["groups"]
    #     groups = {id["id"]: id for id in goal}
    #     return(groups)       

    # def getTickets(self):
    #     groups = self.getGroups()
    #     print("Getting Tickets from " + self.portal)
    #     s = requests.Session()
    #     basic = HTTPBasicAuth(self.api_key, ":X")
    #     tickets = []
    #     page = 1
    #     while page <= 10:
    #         r = s.get(self.portal + "/api/v2/tickets?include=department,requester,stats,tags&per_page=100&page=" + str(page), auth = basic)
    #         # r = s.get(self.portal + "/api/v2/tickets/filter?query=\"group_id:" + str(self.gid) + " AND tag:SentinelOne\"", auth = basic)
    #         w = vars(r)["_content"]
    #         encoding = "utf-8"
    #         p = str(w, encoding)
    #         res = json.loads(p)
    #         goal = res["tickets"]
    #         for i in goal:
    #             if i["group_id"] is not None:
    #                 values = {
    #                     "group_name": groups[i["group_id"]]["name"],
    #                     "@timestamp": self.tstamp
    #                 }
    #             else:
    #                 values = {
    #                     "group_name": None,
    #                     "@timestamp": self.tstamp
    #                 }
    #             i.update(values)
    #         page += 1
    #         tickets.extend(goal)
    #     return(tickets, self.tstamp_str)

    # def createTicketPayload(self, subject, description, tags=[], priority=1, status=2):
        
    #     payload = {
    #         "requester_id": self.id,
    #         "description":  description, 
    #         "subject": subject,
    #         "email": self.email,
    #         "phone": self.phone, 
    #         "priority": priority, 
    #         "status": status, 
    #         "source": 2,
    #         "tags": tags,
    #         "custom_fields": {"ansprechperson_vorname_name": self.ansprechperson}
    #     }

    #     return(payload)

    # def checkTicket(self, payload):
    #     print("Check if Ticket exists: " + payload["subject"])
    #     tickets = self.getTickets()
    #     for i in tickets[0]:
    #         if i["subject"] == payload["subject"]:
    #             return(i)
    #     return

    # def createTicket(self, payload):       
    #     print("Creating Ticket: " + payload["subject"])
    #     s = requests.Session()
    #     basic = HTTPBasicAuth(self.api_key, ":X")
    #     r = s.post(self.portal + "/api/v2/tickets", auth = basic, json = payload)
    #     w = vars(r)["_content"]
    #     encoding = "utf-8"
    #     p = str(w, encoding)
    #     res = json.loads(p)
    #     goal = res["ticket"]
    #     return(goal)

    # def updateTicket(self, id, payload):       
    #     print("Updating Ticket: " + payload["subject"])
    #     s = requests.Session()
    #     basic = HTTPBasicAuth(self.api_key, ":X")
    #     r = s.put(self.portal + "/api/v2/tickets/" + str(id), auth = basic, json = payload)
    #     w = vars(r)["_content"]
    #     encoding = "utf-8"
    #     p = str(w, encoding)
    #     res = json.loads(p)
    #     goal = res["ticket"]
    #     return(goal)