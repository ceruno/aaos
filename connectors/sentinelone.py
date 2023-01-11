import aiohttp
from datetime import datetime, timedelta
import pytz
import time


class SentinelOneAPI:
    def __init__(self, url, token, item):

        self.url = url
        self.apitoken = token
        self.headers = {"Authorization": "ApiToken " + token}
        self.item = item
        self.endpoint = "/web/api/v2.1/" + item
        self.params = {"limit": "1000"}
        if self.item == "groups":
            self.params = {"limit": "200"}
        if self.item in ["exclusions", "restrictions"]:
            self.params.update({"includeChildren": "true", "includeParents": "true"})
        if self.item == "installed-applications":
            self.params.update({"riskLevelsNin": "none"})
        if self.item == "activities":
            self.params.update({"sortOrder": "desc"})

    async def get(self, session):

        async with session.get(self.url + self.endpoint, params=self.params) as resp:

            assert resp.status == 200
            goal = await resp.json()
            result = goal["data"]
            cursor = goal["pagination"]["nextCursor"]

            if "sites" in result:
                result = result["sites"]

            for i in result:
                values = {
                    "@timestamp": self.tstamp,
                    "managementConsoleUrl": self.url,
                    "ts": self.tsns,
                }
                i.update(values)

                if self.item == "activities":
                    i["@timestamp"] = datetime.strptime(
                        i["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    if "current" in i["data"]:
                        i["data"]["current"] = str(i["data"]["current"])
                    if "newValue" in i["data"]:
                        i["data"]["newValue"] = str(i["data"]["newValue"])
                    if "previous" in i["data"]:
                        i["data"]["previous"] = str(i["data"]["previous"])

            return (result, cursor)

    async def getAll(self):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()
        results = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            result = await self.get(session)
            results.extend(result[0])

            while result[1] != None:
                self.params.update({"cursor": result[1]})
                result = await self.get(session)
                results.extend(result[0])

        return results

    async def getByDelta(self, delta):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()
        time = self.tstamp - timedelta(minutes=int(delta))
        time_utc = time.astimezone(pytz.timezone("UTC"))
        time_str = time_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.params.update({"createdAt__gte": time_str})
        results = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            result = await self.get(session)
            results.extend(result[0])

            while result[1] != None:
                self.params.update({"cursor": result[1]})
                result = await self.get(session)
                results.extend(result[0])

        return results

    async def get1000(self):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()

        async with aiohttp.ClientSession(headers=self.headers) as session:
            result = await self.get(session)

        return result[0]

    async def getBySite(self, site):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()
        self.params.update({"siteIds": site["id"]})
        results = []

        if not ((self.item == "installed-applications") and (site["sku"] == "Core")):

            async with aiohttp.ClientSession(headers=self.headers) as session:
                result = await self.get(session)
                results.extend(result[0])

                while result[1] != None:
                    self.params.update({"cursor": result[1]})
                    result = await self.get(session)
                    results.extend(result[0])

                for i in results:
                    values = {
                        "accountId": site["accountId"],
                        "accountName": site["accountName"],
                        "siteId": site["id"],
                        "siteName": site["name"],
                    }
                    i.update(values)

        return results

    async def getByActivityId(self, ids):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()
        self.params.update({"activityTypes": ids})
        time = self.tstamp - timedelta(days=7)
        time_utc = time.astimezone(pytz.timezone("UTC"))
        time_str = time_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.params.update({"createdAt__gte": time_str})
        results = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            result = await self.get(session)
            results.extend(result[0])

            while result[1] != None:
                self.params.update({"cursor": result[1]})
                result = await self.get(session)
                results.extend(result[0])

        return results
