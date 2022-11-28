from elasticsearch import Elasticsearch, helpers
import traceback


class ElasticAPI:
    def __init__(self, config, password, timestamp, index, pipeline):

        self.user = config["user"]
        self.password = password
        self.timestamp = timestamp
        self.index = index
        self.pipeline = pipeline

        if config["elastic_cloud_id"] != "":
            self.cloud_id = config["elastic_cloud_id"]
            self.session = Elasticsearch(
                cloud_id=self.cloud_id,
                basic_auth=(self.user, self.password),
            )
        else:
            if config["elastic_url"] != "":
                self.url = config["elastic_url"]
                if config["tls_fingerprint"] != "":
                    self.fingerprint = config["tls_fingerprint"]
                    self.session = Elasticsearch(
                    self.url,
                    ssl_assert_fingerprint=(self.fingerprint),
                    basic_auth=(self.user, self.password),
                )
                else:
                    self.session = Elasticsearch(
                        self.url, basic_auth=(self.user, self.password)
                    )

    def write(self, results):

        data = [
            {
                "_op_type": "create",
                "_index": self.index,
                "_id": str(node["id"])
                + " - "
                + (node["@timestamp"]).strftime("%d.%m.%Y, %H:%M:%S"),
                "_source": node,
            }
            for node in results
        ]

        if self.pipeline != "":
            for item in data:
                values = {"pipeline": self.pipeline}
                item.update(values)

        if self.timestamp == False:
            for item in data:
                values = {"_id": item["_source"]["id"]}
                item.update(values)

        while True:
            try:
                helpers.bulk(self.session, data)
                break
            except Exception:
                return traceback.format_exc()
        return {"result": "success", "index": self.index}
