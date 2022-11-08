from typing import Any, List, Dict
from web3cli.main import Web3CliTest
from web3cli.core.models.address import Address
import pytest


def test_address_list(addresses: List[Dict[str, Any]]) -> None:
    """Add addresses and check that they are listed alphabetically"""

    # Sort test address alphabetically by label
    addresses = sorted(addresses, key=lambda a: a["label"])
    # Init the CLI app (without launching the command yet)
    argv = ["address", "list"]
    with Web3CliTest(argv=argv) as app:
        # Add the addresses
        for a in addresses:
            Address.create(
                label=a["label"],
                address=a["address"],
            )
        # Run `web3 address list`
        app.run()
        # Catpure output
        data, output = app.last_rendered
        # Test
        for i in range(0, len(addresses)):
            assert data[i][0] == addresses[i]["label"]
            assert data[i][1] == addresses[i]["address"]


def test_address_get(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        argv = [
            "address",
            "get",
            a["label"],
        ]
        with Web3CliTest(argv=argv) as app:
            Address.create(
                label=a["label"],
                address=a["address"],
            )
            app.run()
            data, output = app.last_rendered
            assert data["out"] == a["address"]


def test_address_add(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        argv = [
            "address",
            "add",
            a["label"],
            a["address"],
            "--description",
            a["description"],
        ]
        with Web3CliTest(argv=argv) as app:
            app.run()
            address = Address.get_by_label(a["label"])
            assert Address.select().count() == 1
            assert address.address == a["address"]
            assert address.description == a["description"]


def test_address_update(addresses: List[Dict[str, Any]]) -> None:
    """Create address 0, then update it with the data of address 1,
    while keeping the same label"""
    argv = [
        "address",
        "add",
        addresses[0]["label"],
        addresses[1]["address"],
        "--description",
        addresses[1]["description"],
        "--update",
    ]
    with Web3CliTest(argv=argv) as app:
        Address.create(
            label=addresses[0]["label"],
            address=addresses[0]["address"],
            description=addresses[0]["description"],
        )
        app.run()
        address = Address.get_by_label(addresses[0]["label"])
        assert address.address == addresses[1]["address"]
        assert address.description == addresses[1]["description"]


def test_address_delete(addresses: List[Dict[str, Any]]) -> None:
    for a in addresses:
        argv = [
            "address",
            "delete",
            a["label"],
        ]
        with Web3CliTest(argv=argv) as app:
            Address.create(
                label=a["label"],
                address=a["address"],
            )
            app.run()
            assert Address.select().count() == 0
