from __future__ import annotations
from peewee import SqliteDatabase, Model
from typing import List, Dict, Any

### Database, will be initialized during post_setup hook
db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_all(cls, order_by: Any = None) -> List[Dict[str, Any]]:
        query = cls.select()
        if order_by:
            query = query.order_by(order_by)
        return [m for m in query.dicts()]
