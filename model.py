import peewee
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase("index.db")


class File(peewee.Model):

    sha256sum = peewee.CharField(max_length=70, null=True)
    st_ctime = peewee.DateTimeField(null=True)
    path = peewee.CharField(unique=True, null=True)
    st_size = peewee.IntegerField(null=True)
    is_del = peewee.BooleanField(default=False)

    class Meta:
        database = db


db.connect()
