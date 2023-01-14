from typing import Any

import pytest
from web3.types import ABI

from web3core.exceptions import ContractAbiNotResolved
from web3core.helpers.seed import seed_contract
from web3core.models.contract import Contract, ContractType
from web3core.models.types import ContractFields


# Test resolve_abi() with a contract that does not have an ABI
def test_resolve_abi_without_abi(db: Any, contract_without_abi: ContractFields) -> None:
    contract: Contract = seed_contract(contract_without_abi)
    assert contract.resolve_abi() == ContractType.get_by_name(contract.type).abi


# Test resolve_abi() with a contract that has an ABI
def test_resolve_abi_with_abi(
    db: Any, contract_without_abi: ContractFields, simple_abi: ABI
) -> None:
    contract: Contract = seed_contract(contract_without_abi)
    contract.abi = simple_abi
    contract.save()
    assert contract.resolve_abi() == simple_abi


# Test resolve_abi() with a contract that does not have an ABI and does not have a type
def test_resolve_abi_without_abi_or_type(
    db: Any, contract_without_abi: ContractFields
) -> None:
    contract: Contract = seed_contract(contract_without_abi)
    contract.abi = None
    contract.type = None
    contract.save()
    with pytest.raises(ContractAbiNotResolved):
        contract.resolve_abi()


# Test resolve_abi() with a contract that does not have an ABI and has a type that does not exist
def test_resolve_abi_without_abi_with_missing_type(
    db: Any,
    contract_without_abi: ContractFields,
) -> None:
    contract: Contract = seed_contract(contract_without_abi)
    contract_type_inst = ContractType.get_by_name(contract.type)
    contract_type_inst.delete_instance()
    contract.save()
    with pytest.raises(ContractAbiNotResolved):
        contract.resolve_abi()
