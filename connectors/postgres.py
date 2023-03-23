import json
import psycopg2, psycopg2.extras
from datetime import datetime
import pytz
import time


class PostgresAPI:
    def __init__(self, config, password, query):
        self.host = config["host"]
        self.port = config["port"]
        self.db = config["db"]
        self.user = config["user"]
        self.password = password
        self.query = query
        self.session = psycopg2.connect(
            host=self.host, database=self.db, user=self.user, password=self.password
        )

    async def get(self):

        self.tstamp = datetime.now(tz=pytz.timezone("Europe/Zurich"))
        self.tsns = time.time_ns()

        cur = self.session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(self.query)
        results = cur.fetchall()

        data = []

        for result in results:
            result = dict(result)
            values = {
                "@timestamp": self.tstamp,
                "ts": self.tsns,
            }
            result.update(values)

            match = list(
                filter(
                    lambda i: i["id"] == result["id"],
                    data,
                )
            )

            if match != []:
                match = match[0]
                for key in match.keys():
                    if match[key] != result[key]:
                        if not isinstance(match[key], list):
                            match[key] = [match[key]]
                        match[key].append(result[key])

            else:
                data.append(result)

        return data
