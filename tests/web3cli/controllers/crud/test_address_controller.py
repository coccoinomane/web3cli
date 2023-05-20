from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3core.exceptions import AddressIsInvalid, RecordNotFound
from web3core.helpers.seed import seed_addresses
from web3core.models.address import Address
from web3core.models.types import AddressFields


def test_address_list(addresses: List[AddressFields]) -> None:
    """Add addresses and check that they are listed alphabetically"""

    # Sort test address alphabetically by name
    addresses = sorted(addresses, key=lambda a: a["name"])
    with Web3CliTest() as app:
        # Add the addresses
        seed_addresses(addresses)
        # Run `w3 address list`
        app.set_args(["address", "list"]).run()
        # Catpure output
        data, output = app.last_rendered
        # Test
        for i in range(0, len(addresses)):
            assert data[i][0] == addresses[i]["name"]
            assert data[i][1] == addresses[i]["address"]


def test_address_get(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(addresses)
            app.set_args(
                [
                    "address",
                    "get",
                    a["name"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["name"] == a["name"]
            assert data["address"] == a["address"]


def test_address_add(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "address",
                    "add",
                    a["name"],
                    a["address"],
                    "--desc",
                    a["desc"],
                ]
            ).run()
            address = Address.get_by_name(a["name"])
            assert Address.select().count() == 1
            assert address.address == a["address"]
            assert address.desc == a["desc"]


@pytest.mark.parametrize(
    "invalid_address",
    [
        "0x135A9431374bF1A5Ac05Ac2051a7B1a6e0b26D67",
        "0x135A94q1374bF1A5Ac05Ac2051a7B1a6e0b26D67",
        "a normal string",
    ],
)
def test_address_add_validation(invalid_address: str) -> None:
    with Web3CliTest() as app:
        with pytest.raises(AddressIsInvalid):
            app.set_args(
                [
                    "address",
                    "add",
                    "foo",
                    invalid_address,
                ]
            ).run()


def test_address_update(addresses: List[AddressFields]) -> None:
    """Create address 0, then update it with the data of address 1,
    while keeping the same name"""
    with Web3CliTest() as app:
        seed_addresses([addresses[0]])
        app.set_args(
            argv=[
                "address",
                "add",
                addresses[0]["name"],
                addresses[1]["address"],
                "--desc",
                addresses[1]["desc"],
                "--update",
            ]
        ).run()
        address = Address.get_by_name(addresses[0]["name"])
        assert address.address == addresses[1]["address"]
        assert address.desc == addresses[1]["desc"]


def test_address_delete(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(addresses)
            app.set_args(
                [
                    "address",
                    "delete",
                    a["name"],
                ]
            ).run()
            assert Address.select().count() == len(addresses) - 1
            with pytest.raises(RecordNotFound):
                Address.get_by_name_or_raise(a["name"])
