from __future__ import annotations
from peewee import TextField, BlobField
from web3 import Account
from web3cli.core.helpers.crypto import encrypt_string
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import SignerNotFound


class Signer(BaseModel):
    class Meta:
        table_name = "signers"

    name = TextField(unique=True)
    address = TextField()
    key = BlobField()

    @classmethod
    def create_encrypt(cls, name: str, key: str, pwd: bytes) -> Signer:
        """Create a signer and encrypt its key in one go;
        requires a 32-byte password to use for encrypting the key"""
        address = Account.from_key(key).address
        return Signer.create(name=name, address=address, key=encrypt_string(key, pwd))

    @classmethod
    def get_by_name(cls, name: str) -> Signer:
        """Return the signer object with the given name, or None if
        it does not exist"""
        return cls.get_or_none(cls.name == name)

    @classmethod
    def get_by_name_or_raise(cls, name: str) -> Signer:
        """Return the signer object with the given name; raise
        error if it does not exist"""
        try:
            return cls.get(cls.name == name)
        except:
            raise SignerNotFound(f"Signer '{name}' does not exist")

    @classmethod
    def get_address(cls, name: str) -> str:
        """Return the address of the signer with the given name; raise
        error if the signer does not exist"""
        signer = Signer.get_by_name_or_raise(name)
        return signer.address
