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
    text = pw.CharField()
    entered_at = pw.DateTimeField()
    person_id = pw.ForeignKeyField(Person, related_name="quotes")

    class Meta:
        indexes = (
            (('text', 'person_id'), True),
        )
