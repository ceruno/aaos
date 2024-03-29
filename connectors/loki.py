import datetime
import json
import requests
import re


class LokiAPI:
    def __init__(self, config, token, source, item):

        self.url = re.findall(r"https://(.*)", config["loki_url"])[0]
        self.user = config["user"]
        self.token = token
        self.source = source
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
                        "source": self.source,
                    },
                    "values": values,
                }
            ]
        }

        answer = requests.post(self.connectionstring, json=payload, headers=headers)
        return {"destination": "loki", "result": "success"}
