import pytest
from web3cli.main import Web3CliTest
from web3cli.core.models.address import Address
from web3cli.core.exceptions import AddressNotResolved
from web3cli import resolve_address


def test_balance() -> None:
    argv = ["balance", "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"]
    with Web3CliTest(argv=argv) as app:
        Address.create(
            label="Ethereum foundation",
            address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        )
        # Existing label
        address = resolve_address("Ethereum foundation")
        assert type(address) is str
        assert address == "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
        # Valid address
        address = resolve_address("0x8894e0a0c962cb723c1976a4421c95949be2d4e3")
        assert type(address) is str
        assert address == "0x8894e0a0c962cb723c1976a4421c95949be2d4e3"
        # Invalid address + non-existing label
        with pytest.raises(AddressNotResolved):
            address = resolve_address("0x123")
        with pytest.raises(AddressNotResolved):
            address = resolve_address("non existing label")
