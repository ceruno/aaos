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

        for i in results:
            i = dict(i)
            values = {
                "@timestamp": self.tstamp,
                "ts": self.tsns,
            }
            i.update(values)
            data.append(i)

        return data
