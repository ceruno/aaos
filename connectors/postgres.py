import json
import psycopg2, psycopg2.extras

class PostgresAPI:
    def __init__(self, config, password, item):
        self.host = config["host"]
        self.port = config["port"]
        self.db = config["db"]
        self.user = config["user"]
        self.password = password
        self.query = config["query"]
        self.session = psycopg2.connect(
            host=self.host,
            database = self.db,
            user = self.user,
            password = self.password)

    def get(self):
        cur = self.session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(self.query)
        # cur.execute("select * from public.\"Questionnaire\";")
        results = cur.fetchall()
        #print(json.dumps(results))
        return results
        #conn.rollback()