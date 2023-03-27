import datetime
import requests
import uuid


class DataSetAPI:
    def __init__(self, config, token, source, item):

        self.url = config["dataset_url"]
        self.token = token
        self.source = source
        self.item = item
        self.uuid = uuid.uuid4()

    def write(self, results):

        events = []

        for result in results:
            if isinstance(result["@timestamp"], datetime.datetime) == True:
                result["@timestamp"] = result["@timestamp"].strftime(
                    "%d.%m.%Y, %H:%M:%S"
                )
            event = {
                "ts": result["ts"],
                "attrs": result,
            }
            events.append(event)

        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.token,
        }

        payload = {
            "session": str(self.uuid),
            "sessionInfo": {
                "item": self.item,
                "source": self.source,
            },
            "events": events,
        }

        answer = requests.post(
            self.url + "/api/addEvents", json=payload, headers=headers
        )
        return {"destination": "dataset", "result": "success"}
