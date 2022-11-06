from peewee import TextField
from web3cli.core.models.base_model import BaseModel
from web3cli.core.exceptions import AddressNotFound
import web3


class Address(BaseModel):
    class Meta:
        table_name = "addresses"

    address = TextField()
    label = TextField(unique=True)
    description = TextField(null=True)

    @classmethod
    def get_by_label(cls, label: str) -> BaseModel:
        """Return the address object with the given label, or None if
        it does not exist"""
        return cls.get_or_none(cls.label == label)

    @classmethod
    def is_valid_address(cls, address: str) -> bool:
        """Is the address a valid EVM address?"""
        return web3.main.is_address(address)

    @classmethod
    def is_valid_label(cls, label: str) -> bool:
        """Return True if the given label is ok to be saved in the DB.
        The only constraint is that the label is not a valid address,
        because in that case it would mess up the address resolver"""
        return not cls.is_valid_address(label)

    @classmethod
    def get_address(cls, label: str) -> str:
        """Return the address with the given label; raise error
        if no such address is found"""
        address = Address.get_by_label(label)
        if not address:
            raise AddressNotFound(f"Address '{label}' does not exist")
        return address.address

    @classmethod
    def resolve_address(cls, address_or_label: str) -> str:
        """Return the address with the given label, but if an actual valid
        address is passed (0x...) then return it"""
        return (
            address_or_label
            if cls.is_valid_address(address_or_label)
            else cls.get_address(address_or_label)
        )
