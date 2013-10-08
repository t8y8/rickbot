import sqlite3
import datetime
from models import Person, Quote

db = sqlite3.connect("rick.db")

result = db.execute("SELECT saying, date FROM sayings")

MIGRATE_TABLE = []

for row in result:
	text = row[0].encode("8859", "ignore").decode("utf-8","xmlcharref").replace("“", '"')
	try:
		time = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
	except:
		time = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)
	MIGRATE_TABLE.append((text, time))
db.close()

#print(MIGRATE_TABLE)

rick = Person.get(Person.name == "Rick")

for text, time in MIGRATE_TABLE:
	Quote.create(text=text,
				entered_at=time,
				person_id=rick).save()

test_query = Quote.select().where(Quote.person_id.name == "Rick")

print([i.text for i in test_query])

#datetime.datetime.strptime(ttime, "%Y-%m-%d %H:%M:%S")