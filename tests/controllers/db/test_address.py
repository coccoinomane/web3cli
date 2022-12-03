from typing import Any, List, Dict
from tests.main import Web3CliTest
from web3cli.core.exceptions import AddressIsInvalid
from web3cli.core.models.address import Address
from tests.seeder import seed_addresses
import pytest
from web3cli.core.models.types import AddressFields


def test_address_list(addresses: List[AddressFields]) -> None:
    """Add addresses and check that they are listed alphabetically"""

    # Sort test address alphabetically by name
    addresses = sorted(addresses, key=lambda a: a["name"])
    with Web3CliTest() as app:
        # Add the addresses
        seed_addresses(app, addresses)
        # Run `w3 db address list`
        app.set_args(["db", "address", "list"]).run()
        # Catpure output
        data, output = app.last_rendered
        # Test
        for i in range(0, len(addresses)):
            assert data[i][0] == addresses[i]["name"]
            assert data[i][1] == addresses[i]["address"]


def test_address_get(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(app, addresses)
            app.set_args(
                [
                    "db",
                    "address",
                    "get",
                    a["name"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == a["address"]


def test_address_add(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "db",
                    "address",
                    "add",
                    a["name"],
                    a["address"],
                    "--description",
                    a["description"],
                ]
            ).run()
            address = Address.get_by_name(a["name"])
            assert Address.select().count() == 1
            assert address.address == a["address"]
            assert address.description == a["description"]


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
                    "db",
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
        seed_addresses(app, [addresses[0]])
        app.set_args(
            argv=[
                "db",
                "address",
                "add",
                addresses[0]["name"],
                addresses[1]["address"],
                "--description",
                addresses[1]["description"],
                "--update",
            ]
        ).run()
        address = Address.get_by_name(addresses[0]["name"])
        assert address.address == addresses[1]["address"]
        assert address.description == addresses[1]["description"]


def test_address_delete(addresses: List[AddressFields]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(app, addresses)
            app.set_args(
                [
                    "db",
                    "address",
                    "delete",
                    a["name"],
                ]
            ).run()
            assert Address.select().count() == len(addresses) - 1
