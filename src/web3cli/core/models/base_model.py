from peewee import SqliteDatabase
from peewee import Model

### Database, will be initialized during post_setup hook
db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db
