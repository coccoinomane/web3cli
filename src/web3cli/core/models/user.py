from peewee import TextField
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import UserNotFound


class User(BaseModel):
    class Meta:
        table_name = "users"

    label = TextField(null=True)
    address = TextField()
    key = TextField(unique=True)

    @classmethod
    def get_by_label(cls, label: str) -> BaseModel:
        """Return the user object with the given label, or None if
        it does not exist"""
        return cls.get_or_none(cls.label == label)

    @classmethod
    def get_address(cls, label: str) -> str:
        """Return the address of the user with the given label; raise
        error if no such address is found"""
        user = User.get_by_label(label)
        if not user:
            raise UserNotFound(f"User '{label}' does not exist")
        return user.address
