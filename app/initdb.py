import peewee as pw
from models import *
from datetime import datetime

Person.drop_table(True)
Quote.drop_table(True)

Person.create_table()
Quote.create_table()

Person.create(name="Rick").save()
Person.create(name="Joel").save()

rick = Person.get(Person.name == "Rick")
joel = Person.get(Person.name == "Joel")

Quote.create(text="Golly Gee, quotes are the best!", entered_at=datetime.now(), person_id=rick).save()
Quote.create(text="America is a pretty cool place", entered_at=datetime.now(), person_id=joel).save()
Quote.create(text="Derp derp derp. Wow.", entered_at=datetime.now(), person_id=rick).save()
