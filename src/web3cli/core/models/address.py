from __future__ import annotations
from typing import Type
from peewee import TextField
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import (
    AddressIsInvalid,
    AddressNotFound,
    AddressNotResolved,
)
import web3
from web3cli.core.models.types import AddressFields
from playhouse.shortcuts import update_model_from_dict
from playhouse.signals import pre_save
from web3cli.core.types import Logger


class Address(BaseModel):
    class Meta:
        table_name = "addresses"

    address = TextField()
    name = TextField(unique=True)
    description = TextField(null=True)

    @classmethod
    def get_by_name(cls, name: str) -> Address:
        """Return the address object with the given name, or None if
        it does not exist"""
        return cls.get_or_none(cls.name == name)

    @classmethod
    def get_by_name_or_raise(cls, name: str) -> Address:
        """Return the address object with the given name; raise
        error if it does not exist"""
        try:
            return cls.get(cls.name == name)
        except:
            raise AddressNotFound(f"Address '{name}' does not exist")

    @classmethod
    def upsert(cls, fields: AddressFields, logger: Logger = None) -> Address:
        """Create an address, or replace it if an address with the same
        name already exists, maintaining its ID and relations."""
        address: Address = Address.get_or_none(name=fields["name"])
        if address:
            address = update_model_from_dict(address, fields)
            if logger:
                logger(f"Address {address.name} updated")
        else:
            address = Address(**fields)
            if logger:
                logger(f"Address {address.name} created")
        address.save()
        return address

    @classmethod
    def is_valid_address(cls, address: str) -> bool:
        """Is the address a valid EVM address?"""
        return web3.main.is_address(address)

    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        """Return True if the given name is ok to be saved in the DB.
        The only constraint is that the name is not a valid address,
        because in that case it would mess up the address resolver"""
        return not cls.is_valid_address(name)

    @classmethod
    def get_address(cls, name: str) -> str:
        """Return the address with the given name; raise error
        if no such address is found"""
        address = Address.get_by_name_or_raise(name)
        return address.address

    @classmethod
    def resolve_address(cls, address_or_name: str) -> str:
        """Return the address with the given name, but if an actual valid
        address is passed (0x...) then return it"""
        try:
            return (
                address_or_name
                if cls.is_valid_address(address_or_name)
                else cls.get_address(address_or_name)
            )
        except AddressNotFound:
            raise AddressNotResolved(
                f"Could not resolve '{address_or_name}': neither a valid address nor a name of a stored address"
            )


@pre_save(sender=Address)
def validate(model_class: Address, instance: Type[Address], created: bool) -> None:
    """Validate the address which is about to be saved"""
    if not Address.is_valid_address(instance.address):
        raise AddressIsInvalid(f"Invalid address given: {instance.address}")
