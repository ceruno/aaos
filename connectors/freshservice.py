import aiohttp
import base64
import math
import pytz
from datetime import datetime


class FreshServiceAPI:
    def __init__(self, config, api_key, item):

        self.url = config["fresh_url"]
        self.api_key = api_key
        self.item = item
        self.endpoint = "/api/v2/" + item
        self.params = {"per_page": "100"}
        self.gid = config["group_id"]
        self.id = config["requester_id"]
        self.email = config["requester_email"]
        self.phone = config["requester_phone"]
        self.ansprechperson = config["ansprechperson"]
        if item == "tickets":
            self.params.update({"include": "department,requester,stats,tags"})

    async def get(self, session):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))

        async with session.get(self.url + self.endpoint, params=self.params) as resp:

            assert resp.status == 200
            goal = await resp.json()
            result = goal[self.item]
            link = resp.links.get("next")

            for i in result:
                values = {
                    "@timestamp": self.tstamp,
                }
                i.update(values)

            return (result, link)

    async def getAll(self, groups=None):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        results = []
        page = 1

        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(self.api_key, "X")
        ) as session:
            result = await self.get(session)
            results.extend(result[0])

            while result[1] != None:
                page += 1
                self.params.update({"page": page})
                result = await self.get(session)
                results.extend(result[0])

            if groups != None:
                groups_id = {id["id"]: id for id in groups}
                for i in results:
                    if i["group_id"] != None:
                        values = {
                            "group_name": groups_id[i["group_id"]]["name"],
                        }
                    else:
                        values = {
                            "group_name": None,
                        }
                    i.update(values)

        return results

    async def createPayload(self, subject, description, tags=[], priority=1, status=2):

        payload = {
            "requester_id": self.id,
            "description": description,
            "subject": subject,
            "email": self.email,
            "phone": self.phone,
            "priority": priority,
            "status": status,
            "source": 2,
            "tags": tags,
            "custom_fields": {"ansprechperson_vorname_name": self.ansprechperson},
        }

        return payload

    async def checkTicket(self, payload):
        tickets = self.getAll()
        for i in tickets:
            if (i["subject"] == payload["subject"]) and (
                (i["status"] == 2) or (i["status"] == 3)
            ):
                return i
        return

    async def postTicket(self, payload):

        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(self.api_key, "X")
        ) as session:
            async with session.post(self.url + self.endpoint, json=payload) as resp:
                assert resp.status == 200
                goal = await resp.json()
                result = goal["ticket"]
                return result

    async def putTicket(self, payload, id):

        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(self.api_key, "X")
        ) as session:
            async with session.put(
                self.url + self.endpoint + "/" + str(id), json=payload
            ) as resp:
                assert resp.status == 200
                goal = await resp.json()
                result = goal["ticket"]
                return result
