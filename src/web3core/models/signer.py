from __future__ import annotations

from peewee import BlobField, TextField
from web3 import Account

from web3core.helpers.crypto import encrypt_string
from web3core.models.base_model import BaseModel


class Signer(BaseModel):
    class Meta:
        table_name = "signers"

    name = TextField(unique=True)
    address = TextField()
    key = BlobField()

    def get_by_address(address: str) -> Signer:
        """Return the first signer with the given address, or None if
        it does not exist"""
        return Signer.get_or_none(Signer.address == address)

    @classmethod
    def create_encrypt(cls, name: str, key: str, pwd: bytes) -> Signer:
        """Create a signer with encryped private key"""
        return cls.instantiate_encrypt(name, key, pwd).save()

    @classmethod
    def instantiate_encrypt(cls, name: str, key: str, pwd: bytes) -> Signer:
        """Return a signer object without adding it to the database;
        its private key will be encrypted with the given 32-byte password"""
        address = Account.from_key(key).address
        return Signer(name=name, address=address, key=encrypt_string(key, pwd))

    @classmethod
    def get_address(cls, name: str) -> str:
        """Return the address of the signer with the given name; raise
        error if the signer does not exist"""
        signer = Signer.get_by_name_or_raise(name)
        return signer.address
