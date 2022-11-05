from peewee import TextField
from web3cli.core.models.base_model import BaseModel


class Address(BaseModel):
    class Meta:
        table_name = "addresses"

    address = TextField()
    label = TextField(unique=True)
    description = TextField(null=True)

    @classmethod
    def get_by_label(cls, label: str) -> BaseModel:
        """Return the address with the given label, or None if
        it does not exist"""
        return cls.get_or_none(cls.label == label)
