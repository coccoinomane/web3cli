from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import Web3CliError
from web3core.exceptions import ContractNotFound
from web3core.helpers.os import read_json
from web3core.helpers.seed import seed_chains, seed_contracts
from web3core.models.contract import Contract
from web3core.models.types import ChainFields, ContractFields


def test_contract_list(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    """Add contracts and check that they are listed alphabetically
    by name and chain"""
    contracts = sorted(contracts, key=lambda c: c["name"])
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            chain_contracts = [c for c in contracts if c["chain"] == chain["name"]]
            app.set_args(["contract", "list", "-c", chain["name"]]).run()
            data, output = app.last_rendered
            for i in range(0, len(chain_contracts)):
                assert data[i][0] == chain_contracts[i]["name"]
                assert data[i][1] == str(chain_contracts[i]["chain"])
                assert data[i][2] == str(chain_contracts[i]["type"])
                assert data[i][4] == str(chain_contracts[i]["address"])


def test_contract_list_with_type(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    """Add contracts and check that they are listed alphabetically
    by name and chain"""
    contract_type = "erc20"
    contracts = sorted(contracts, key=lambda c: c["name"])
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            chain_contracts = [
                c
                for c in contracts
                if c["chain"] == chain["name"] and c["type"] == contract_type
            ]
            app.set_args(["contract", "list", contract_type, "-c", chain["name"]]).run()
            data, output = app.last_rendered
            for i in range(0, len(chain_contracts)):
                assert data[i][0] == chain_contracts[i]["name"]
                assert data[i][1] == str(chain_contracts[i]["chain"])
                assert data[i][2] == str(chain_contracts[i]["type"])
                assert data[i][4] == str(chain_contracts[i]["address"])


def test_contract_get(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    for c in contracts:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            app.set_args(
                [
                    "contract",
                    "get",
                    c["name"],
                    "--chain",
                    c["chain"],
                ]
            ).run()
            data, output = app.last_rendered
            assert c["name"] in output
            assert c["chain"] in output
            assert c["type"] in output
            assert c["address"] in output


def test_contract_add(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    for c in contracts:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(
                [
                    "contract",
                    "add",
                    c["name"],
                    c["address"],
                    "--desc",
                    c["desc"],
                    "--type",
                    c["type"],
                    "--chain",
                    c["chain"],
                ]
            ).run()
            contract = Contract.get_by_name_and_chain(c["name"], c["chain"])
            assert contract.select().count() == 1
            assert Contract.name == c["name"]
            assert Contract.desc == c["desc"]
            assert Contract.type == c["type"]
            assert Contract.address == c["address"]


# If neither --type nor --abi is provided, should throw an error
def test_contract_add_without_abi_and_type(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    c = contracts[0]
    with pytest.raises(Web3CliError, match="Either --type or --abi must be provided"):
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(
                [
                    "contract",
                    "add",
                    c["name"],
                    c["address"],
                    "--desc",
                    c["desc"],
                    "--chain",
                    c["chain"],
                ]
            ).run()


# Test that a contract can be added with an ABI as a string
def test_contract_add_with_abi_string(
    contracts: List[ContractFields], chains: List[ChainFields], erc20_abi_string: str
) -> None:
    c = contracts[0]
    with Web3CliTest() as app:
        seed_chains(chains)
        app.set_args(
            [
                "contract",
                "add",
                c["name"],
                c["address"],
                "--desc",
                c["desc"],
                "--abi",
                erc20_abi_string,
                "--chain",
                c["chain"],
            ]
        ).run()
        contract = Contract.get_by_name_and_chain(c["name"], c["chain"])
        assert contract.select().count() == 1
        assert Contract.name == c["name"]
        assert Contract.desc == c["desc"]
        assert Contract.type == c["type"]
        assert Contract.address == c["address"]
        assert Contract.abi == erc20_abi_string


# Test that a contract can be added with an ABI from a file
def test_contract_add_with_abi_file(
    contracts: List[ContractFields], chains: List[ChainFields], erc20_abi_file: str
) -> None:
    c = contracts[0]
    with Web3CliTest() as app:
        seed_chains(chains)
        app.set_args(
            [
                "contract",
                "add",
                c["name"],
                c["address"],
                "--desc",
                c["desc"],
                "--abi",
                erc20_abi_file,
                "--chain",
                c["chain"],
            ]
        ).run()
        contract = Contract.get_by_name_and_chain(c["name"], c["chain"])
        assert contract.select().count() == 1
        assert Contract.name == c["name"]
        assert Contract.desc == c["desc"]
        assert Contract.type == c["type"]
        assert Contract.address == c["address"]
        assert Contract.abi == read_json(erc20_abi_file)


def test_contract_update(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    """Create contract 0, then update it with the data of contract 1,
    while keeping the same name and chain"""
    with Web3CliTest() as app:
        seed_chains(chains)
        seed_contracts([contracts[0]])
        app.set_args(
            argv=[
                "contract",
                "add",
                contracts[0]["name"],
                contracts[1]["address"],
                "--desc",
                contracts[1]["desc"],
                "--type",
                contracts[1]["type"],
                "--update",
                "--chain",
                contracts[0]["chain"],
            ]
        ).run()
        contract = Contract.get_by_name_and_chain(
            contracts[0]["name"], contracts[0]["chain"]
        )
        assert Contract.desc == contracts[1]["desc"]
        assert Contract.type == contracts[1]["type"]
        assert Contract.address == contracts[1]["address"]


def test_contract_delete(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    for c in contracts:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            app.set_args(
                [
                    "contract",
                    "delete",
                    c["name"],
                    "--chain",
                    c["chain"],
                ]
            ).run()
            assert Contract.select().count() == len(contracts) - 1
            with pytest.raises(ContractNotFound):
                Contract.get_by_name_and_chain_or_raise(c["name"], c["chain"])
