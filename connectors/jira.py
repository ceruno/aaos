import aiohttp
import base64
import pytz
import time
from datetime import datetime


class JiraAPI:
    def __init__(self, config, token, args):

        self.url = config["jira_url"]
        self.user = config["user"]
        self.token = token
        self.item = args["item"]
        self.endpoint = "/rest/api/3/search"
        if "jql" in args:
            self.params = {
                "jql": args["jql"],
                "startAt": 0,
                "maxResults": 100,
                "fields": "*all",
            }
        if "project" in args:
            self.project = args["project"]
            self.params = {
                "jql": "project=" + self.project,
                "startAt": 0,
                "maxResults": 100,
                "fields": "*all",
            }
        self.credentials = f"{self.user}:{self.token}"
        self.credentials_enc = base64.b64encode(self.credentials.encode()).decode(
            "ascii"
        )
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.credentials_enc }",
        }

    async def get(self, session):

        async with session.get(self.url + self.endpoint, params=self.params) as resp:

            assert resp.status == 200
            goal = await resp.json()
            result = goal[self.item]
            total = goal["total"]

            for i in result:
                values = {
                    "@timestamp": self.tstamp,
                    "ts": self.tsns,
                }
                i.update(values)

            return (result, total)

    async def getAll(self):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()
        results = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            result = await self.get(session)
            results.extend(result[0])

            while self.params["startAt"] <= result[1]:
                self.params["startAt"] += 100
                result = await self.get(session)
                results.extend(result[0])

        return results

    async def createPayload(self, subject, description, labels):

        payload = {
            "fields": {
                "project": {"key": self.project},
                "summary": subject,
                "description": description,
                "issuetype": {"name": "Task"},
                "labels": labels,
            }
        }

        return payload

    async def checkIssue(self, payload):
        tickets = self.getAll()
        for i in tickets:
            if (i["fields"]["summary"] == payload["summary"]) and (
                (i["status"]["statusCategory"]["id"] == 3)
                or (i["status"]["statusCategory"]["id"] == 3)
            ):
                return i
        return

    async def postIssue(self, payload):

        self.endpoint = "/rest/api/3/issue"

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url + self.endpoint, json=payload) as resp:
                assert resp.status == 201
                goal = await resp.json()
                result = goal["key"]
                return result

    async def putIssue(self, payload, id):

        self.endpoint = "/rest/api/3/issue"

        payload["update"] = {"description": [{"set": payload["fields"]["description"]}]}
        del payload["fields"]

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.put(
                self.url + self.endpoint + "/" + str(id), json=payload
            ) as resp:
                assert resp.status == 204
                result = await resp.json()
                return result
