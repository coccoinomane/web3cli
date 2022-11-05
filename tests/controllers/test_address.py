from web3cli.main import Web3CliTest
from web3cli.core.models.address import Address


def test_address_add() -> None:
    argv = [
        "address",
        "add",
        "Ethereum foundation",
        "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        "--description",
        "Description",
    ]
    with Web3CliTest(argv=argv) as app:
        app.run()
        address = Address.get_by_label("Ethereum foundation")
        assert Address.select().count() == 1
        assert address.address == "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
        assert address.description == "Description"


def test_address_update() -> None:
    argv = [
        "address",
        "add",
        "Ethereum foundation",
        "0x8894e0a0c962cb723c1976a4421c95949be2d4e3",
        "--description",
        "New description",
        "--update",
    ]
    with Web3CliTest(argv=argv) as app:
        Address.create(
            label="Ethereum foundation",
            address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
            description="Old description",
        )
        app.run()
        address = Address.get_by_label("Ethereum foundation")
        assert address.address == "0x8894e0a0c962cb723c1976a4421c95949be2d4e3"
        assert address.description == "New description"


def test_address_list() -> None:
    argv = ["address", "list"]
    with Web3CliTest(argv=argv) as app:
        Address.create(
            label="Ethereum foundation",
            address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        )
        app.run()
        data, output = app.last_rendered
        assert data[0][0] == "Ethereum foundation"
        assert data[0][1] == "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"


def test_address_delete() -> None:
    argv = [
        "address",
        "delete",
        "Ethereum foundation",
    ]
    with Web3CliTest(argv=argv) as app:
        Address.create(
            label="Ethereum foundation",
            address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        )
        app.run()
        assert Address.select().count() == 0
