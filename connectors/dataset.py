import aiohttp
from datetime import datetime, timedelta
import json
import pytz
import requests
import re
import time
import uuid


class DataSetAPI:
    def __init__(self, config, token, item):

        self.url = config["dataset_url"]
        self.token = token
        self.item = item
        self.uuid = uuid.uuid4()

    def write(self, results):

        events = []
        time_nanosec = time.time_ns()

        for result in results:
            result["@timestamp"] = result["@timestamp"].strftime("%d.%m.%Y, %H:%M:%S")
            event =       {
                # "thread": "1",
                "ts": time_nanosec,
                # "sev": 3,
                "attrs": result
            }
            events.append(event)

        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.token
        }

        payload = {
            "session": str(self.uuid),
            "sessionInfo": {
            "item": self.item,
            "managementConsoleUrl": results[0]["managementConsoleUrl"]
            },
            "events": events
        }

        answer = requests.post(self.url + "/api/addEvents", json=payload, headers=headers)
        return {"result": "success"}