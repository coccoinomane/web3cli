from peewee import TextField
from web3cli.core.models.base_model import BaseModel


class User(BaseModel):
    class Meta:
        table_name = "users"

    label = TextField(null=True)
    address = TextField()
    key = TextField(unique=True)
