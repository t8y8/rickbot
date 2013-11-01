from rick import Person, Quote
from datetime import datetime


def main():
	Person.drop_table(True)
	Quote.drop_table(True)

	Person.create_table()
	Quote.create_table()

	Person.create(name="Rick").save()
	Person.create(name="Joel").save()
	Person.create(name="Rebecca").save()

	rick = Person.get(Person.name == "Rick")
	joel = Person.get(Person.name == "Joel")
	rebecca = Person.get(Person.name == "Rebecca")

	Quote.create(text="Golly Gee, quotes are the best!", entered_at=datetime.now(), person_id=rick).save()
	Quote.create(text="America is a pretty cool place", entered_at=datetime.now(), person_id=joel).save()
	Quote.create(text="Derp derp derp. Wow.", entered_at=datetime.now(), person_id=rick).save()
	Quote.create(text="I hate the things.", entered_at=datetime.now(), person_id=rebecca).save()
	Quote.create(text="What does the fox say", entered_at=datetime.now(), person_id=rick).save()

if __name__ == '__main__':
	main()