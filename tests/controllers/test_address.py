from typing import Any, List, Dict
from tests.main import Web3CliTest
from web3cli.core.models.address import Address
from tests.seeder import seed_addresses


def test_address_list(addresses: List[Dict[str, Any]]) -> None:
    """Add addresses and check that they are listed alphabetically"""

    # Sort test address alphabetically by label
    addresses = sorted(addresses, key=lambda a: a["label"])
    with Web3CliTest() as app:
        # Add the addresses
        seed_addresses(app, addresses)
        # Run `web3 address list`
        app.set_args(["address", "list"]).run()
        # Catpure output
        data, output = app.last_rendered
        # Test
        for i in range(0, len(addresses)):
            assert data[i][0] == addresses[i]["label"]
            assert data[i][1] == addresses[i]["address"]


def test_address_get(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(app, addresses)
            app.set_args(
                [
                    "address",
                    "get",
                    a["label"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == a["address"]


def test_address_add(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "address",
                    "add",
                    a["label"],
                    a["address"],
                    "--description",
                    a["description"],
                ]
            ).run()
            address = Address.get_by_label(a["label"])
            assert Address.select().count() == 1
            assert address.address == a["address"]
            assert address.description == a["description"]


def test_address_update(addresses: List[Dict[str, Any]]) -> None:
    """Create address 0, then update it with the data of address 1,
    while keeping the same label"""
    with Web3CliTest() as app:
        seed_addresses(app, [addresses[0]])
        app.set_args(
            argv=[
                "address",
                "add",
                addresses[0]["label"],
                addresses[1]["address"],
                "--description",
                addresses[1]["description"],
                "--update",
            ]
        ).run()
        address = Address.get_by_label(addresses[0]["label"])
        assert address.address == addresses[1]["address"]
        assert address.description == addresses[1]["description"]


def test_address_delete(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        with Web3CliTest() as app:
            seed_addresses(app, addresses)
            app.set_args(
                [
                    "address",
                    "delete",
                    a["label"],
                ]
            ).run()
            assert Address.select().count() == len(addresses) - 1
