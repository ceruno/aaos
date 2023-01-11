import datetime
import json
import requests
import re
import time


class LokiAPI:
    def __init__(self, config, token, item):

        self.url = re.findall(r"https://(.*)", config["loki_url"])[0]
        self.user = config["user"]
        self.token = token
        self.item = item
        self.connectionstring = (
            "https://"
            + self.user
            + ":"
            + self.token
            + "@"
            + self.url
            + "/loki/api/v1/push"
        )

    def write(self, results):

        time_nanosec = time.time_ns()

        values = []

        for result in results:
            if isinstance(result["@timestamp"], datetime.datetime) == True:
                result["@timestamp"] = result["@timestamp"].strftime(
                    "%d.%m.%Y, %H:%M:%S"
                )
            values.append([str(result["ts"]), json.dumps(result)])

        headers = {"Content-type": "application/json"}

        payload = {
            "streams": [
                {
                    "stream": {
                        "item": self.item,
                        "managementConsoleUrl": results[0]["managementConsoleUrl"],
                    },
                    "values": values,
                }
            ]
        }

        answer = requests.post(self.connectionstring, json=payload, headers=headers)
        return {"destination": "loki", "result": "success"}
