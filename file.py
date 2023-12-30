import psycopg2
import dbconf

conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

cursor = conn.cursor()

#cursor.execute("INSERT INTO public.items_classes (class_name) values ('מוצרי חלב')")

#conn.commit()

#cursor.execute("SELECT * FROM public.items_classes ORDER BY id ASC")
cursor.execute("SELECT * FROM items ORDER BY id ASC")

res = cursor.fetchall()

print(res)
#for line in res:
#    (id, class_name, num_of_objects, date) = line
#    print(f"{id} - {class_name}")



conn.close()