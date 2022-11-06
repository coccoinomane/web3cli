from peewee import TextField
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import SignerNotFound


class Signer(BaseModel):
    class Meta:
        table_name = "signers"

    label = TextField(null=True)
    address = TextField()
    key = TextField(unique=True)

    @classmethod
    def get_by_label(cls, label: str) -> BaseModel:
        """Return the signer object with the given label, or None if
        it does not exist"""
        return cls.get_or_none(cls.label == label)

    @classmethod
    def get_address(cls, label: str) -> str:
        """Return the address of the signer with the given label; raise
        error if no such address is found"""
        signer = Signer.get_by_label(label)
        if not signer:
            raise SignerNotFound(f"Signer '{label}' does not exist")
        return signer.address
