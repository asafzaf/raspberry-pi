import psycopg2
import dbconf

conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

cursor = conn.cursor()

cursor.execute("SELECT * FROM public.items_classes ORDER BY id ASC")

print(cursor.fetchall())