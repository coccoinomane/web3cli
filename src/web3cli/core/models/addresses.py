from peewee import TextField, CharField
from web3cli.core.models.base_model import BaseModel


class Addresses(BaseModel):
    label = TextField()
    description = TextField()
    address = CharField(42)
