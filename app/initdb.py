import peewee as pw
from models import *
from datetime import datetime

Person.drop_table()
Quote.drop_table()

Person.create_table()
Quote.create_table()

Person.create(name="Rick").save()
Person.create(name="Tyler").save()
Person.create(name="Evan").save()

rick = Person.get(Person.name == "Rick")
tyler = Person.get(Person.name == "Tyler")

Quote.create(text="Golly Gee, quotes are the best!", entered_at=datetime.now(), person_id=rick).save()
Quote.create(text="America is a pretty cool place", entered_at=datetime.now(), person_id=tyler).save()
Quote.create(text="Derp derp derp. Wow.", entered_at=datetime.now(), person_id=rick).save()
