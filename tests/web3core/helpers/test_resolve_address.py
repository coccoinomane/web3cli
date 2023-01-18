import secrets
from typing import Any, Dict, List

import pytest

from tests.helper import get_random_string
from web3core.exceptions import AddressNotResolved
from web3core.helpers.resolve import resolve_address
from web3core.helpers.seed import seed_addresses, seed_contracts, seed_signers
from web3core.models.address import Address
from web3core.models.contract import Contract
from web3core.models.signer import Signer
from web3core.models.types import AddressFields, ContractFields


def test_with_valid_address() -> None:
    """Resolve a valid address which is not in the DB by its value"""
    address = resolve_address("0xd0111cF5bF230832F422dA1C6c1D0A512D4e005A")
    assert type(address) is str
    assert address == "0xd0111cF5bF230832F422dA1C6c1D0A512D4e005A"


def test_with_invalid_address_or_name(db: Any, addresses: List[AddressFields]) -> None:
    """Resolve either an invalid address by its value, or a name that
    does not exist in the DB"""
    with pytest.raises(AddressNotResolved):
        resolve_address("non existing name", [Address, Signer])


def test_without_chain_parameter(db: Any, addresses: List[AddressFields]) -> None:
    """Raise error when called on a chain-aware model without specifying
    the chain"""
    with pytest.raises(ValueError):
        resolve_address("whatever", [Contract], chain=None)


def test_on_addresses_table(db: Any, addresses: List[AddressFields]) -> None:
    """Resolve existing addresses in the address table"""
    seed_addresses(addresses)
    for a in addresses:
        address = resolve_address(a["name"], [Address])
        assert type(address) is str
        assert address == a["address"]
        with pytest.raises(Exception):
            address = resolve_address(a["name"], [Signer])


def test_on_signers_table(db: Any, signers: List[Dict[str, Any]]) -> None:
    """Resolve existing addresses in the signers table"""
    seed_signers(signers, secrets.token_bytes(32))
    for s in signers:
        address = resolve_address(s["name"], [Signer])
        assert type(address) is str
        assert address == s["address"]
        with pytest.raises(AddressNotResolved):
            address = resolve_address(s["name"], [Address])


def test_on_contracts_table(db: Any, contracts: List[ContractFields]) -> None:
    """Resolve existing addresses in the contracts table, which is
    chain-aware, so the chain must be specified"""
    seed_contracts(contracts)
    for c in contracts:
        address = resolve_address(c["name"], [Contract], chain=c["chain"])
        assert type(address) is str
        assert address == c["address"]
        with pytest.raises(AddressNotResolved):
            address = resolve_address(c["name"], [Address, Signer])


# Test that if all three records exist (address, signer, contract)
# with the same name, then the 0x address is returned in the right
# order of precedence
def test_resolve_address_priority(
    db: Any,
    addresses: List[AddressFields],
    signers: List[Dict[str, Any]],
    contracts: List[ContractFields],
) -> None:
    same_name = f"same random name {get_random_string()}"
    # Create address record with same name
    seed_addresses(addresses)
    address = Address.select().first()
    address.name = same_name
    address.address = "0x28C6c06298d514Db089934071355E5743bf21d60"
    address.save()
    # Create signer record with same name
    seed_signers(signers, secrets.token_bytes(32))
    signer = Signer.select().first()
    signer.name = same_name
    signer.address = "0xCEc1B92d9eC15fBb337a615c586f10Bc214515df"
    signer.save()
    # Create contract record with same name
    seed_contracts(contracts)
    contract = Contract.select().first()
    contract.name = same_name
    contract.address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    contract.save()
    # Check that the first in the list always wins
    assert (
        resolve_address(same_name, [Address, Signer, Contract], chain=contract.chain)
        == address.address
    )
    assert (
        resolve_address(same_name, [Signer, Contract, Address], chain=contract.chain)
        == signer.address
    )
    assert (
        resolve_address(same_name, [Contract, Address, Signer], chain=contract.chain)
        == contract.address
    )
