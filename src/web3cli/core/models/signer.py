from peewee import TextField, BlobField
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import SignerNotFound


class Signer(BaseModel):
    class Meta:
        table_name = "signers"

    label = TextField(unique=True)
    address = TextField()
    key = BlobField()

    @classmethod
    def get_by_label(cls, label: str) -> BaseModel:
        """Return the signer object with the given label, or None if
        it does not exist"""
        return cls.get_or_none(cls.label == label)

    @classmethod
    def get_by_label_or_raise(cls, label: str) -> BaseModel:
        """Return the signer object with the given label; raise
        error if it does not exist"""
        try:
            return cls.get(cls.label == label)
        except:
            raise SignerNotFound(f"Signer '{label}' does not exist")

    @classmethod
    def get_address(cls, label: str) -> str:
        """Return the address of the signer with the given label; raise
        error if the signer does not exist"""
        signer = Signer.get_by_label_or_raise(label)
        return signer.address
