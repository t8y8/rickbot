# imports
import sqlite3
import datetime
from models import Person, Quote


# old database
db = sqlite3.connect("rick.db")


# make schema on new database
Person.drop_table(True)
Quote.drop_table(True)

Person.create_table()
Quote.create_table()


# make Rick, he's the only one for now
Person.create(name="Rick").save()

# get all the current rows from rick.db
result = db.execute("SELECT saying, date FROM sayings")

# hold the results
MIGRATE_TABLE = []

# do the magic
for row in result:
	# clean dirty text once and for all
	text = row[0].encode("8859", "ignore").decode("utf-8","xmlcharref").replace("“", '"')
	try:
		time = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") # no microseconds
	except:
		time = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0) # seriously, no microseconds
	MIGRATE_TABLE.append((text, time))
db.close()

# rick's got a lot of talking to do
rick = Person.get(Person.name == "Rick")

# MIGRATE
for text, time in MIGRATE_TABLE:
	Quote.create(text=text,
				entered_at=time,
				person_id=rick).save()

# did it work?
test_query = Quote.select().where(Quote.person_id == rick)
print([i.text for i in test_query])