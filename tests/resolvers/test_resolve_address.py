from typing import Any, Dict, List
import pytest
from tests.seeder import seed_addresses
from tests.main import Web3CliTest
from web3cli.core.models.address import Address
from web3cli.core.exceptions import AddressNotResolved
from web3cli.core.models.types import AddressFields


def test_resolve_existing_address(addresses: List[AddressFields]) -> None:
    """Resolve an existing address by its name"""
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(app, addresses)
            address = Address.resolve_address(a["address"])
            assert type(address) is str
            assert address == a["address"]


def test_resolve_valid_address(addresses: List[AddressFields]) -> None:
    """Resolve a valid address which is not in the DB by its value"""
    with Web3CliTest() as app:
        seed_addresses(app, addresses)
        address = Address.resolve_address("0xd0111cF5bF230832F422dA1C6c1D0A512D4e005A")
        assert type(address) is str
        assert address == "0xd0111cF5bF230832F422dA1C6c1D0A512D4e005A"


def test_resolve_invalid_address_or_name(addresses: List[AddressFields]) -> None:
    """Resolve either an invalid address by its value, or a name that
    does not exist in the DB"""
    with Web3CliTest() as app:
        seed_addresses(app, addresses)
        with pytest.raises(AddressNotResolved):
            Address.resolve_address("0x123")
        with pytest.raises(AddressNotResolved):
            Address.resolve_address("non existing name")
