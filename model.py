import peewee
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase("index.db")


class File(peewee.Model):

    sha256sum = peewee.CharField(unique=True, max_length=70, null=True)
    st_ctime = peewee.DateTimeField(null=True)
    path = peewee.CharField(unique=True)
    st_size = peewee.IntegerField(null=True)

    class Meta:
        database = db


db.connect()