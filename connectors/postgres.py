import json
import psycopg2, psycopg2.extras

conn = psycopg2.connect(
    host="db",
    database="sar-dev",
    user="sar-dev",
    password="")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("select * from public.\"Questionnaire\";")
results = cur.fetchall()
print(json.dumps(results))

conn.rollback()