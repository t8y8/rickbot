import peewee as pw

db = pw.SqliteDatabase("quotes.db")

class BaseModel(pw.Model):
    class Meta:
        database = db

class Person(BaseModel):
    name = pw.CharField(unique=True)
    id = pw.PrimaryKeyField()

class Quote(BaseModel):
    id = pw.PrimaryKeyField()
    text = pw.CharField(unique=True)
    entered_at = pw.DateTimeField()
    person_id = pw.ForeignKeyField(Person, related_name="quotes")

    def get_random():
        return Quote.select().order_by(pw.fn.random()).limit(1)