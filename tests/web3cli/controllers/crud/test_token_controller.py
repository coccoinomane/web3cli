from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3core.exceptions import ContractNotFound
from web3core.helpers.seed import seed_chains, seed_contracts
from web3core.models.contract import Contract
from web3core.models.types import ChainFields, ContractFields


def test_token_list(contracts: List[ContractFields], chains: List[ChainFields]) -> None:
    """Add contracts and check that they are listed alphabetically
    by name and chain"""
    contracts = sorted(contracts, key=lambda c: c["name"])
    for chain in chains:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            chain_tokens = [
                c
                for c in contracts
                if c["chain"] == chain["name"] and c["type"] == "erc20"
            ]
            app.set_args(["token", "list", "-c", chain["name"]]).run()
            data, output = app.last_rendered
            for i in range(0, len(chain_tokens)):
                assert data[i][0] == chain_tokens[i]["name"]
                assert data[i][1] == str(chain_tokens[i]["chain"])
                assert data[i][2] == str(chain_tokens[i]["type"])
                assert data[i][4] == str(chain_tokens[i]["address"])


def test_token_add(contracts: List[ContractFields], chains: List[ChainFields]) -> None:
    tokens = [c for c in contracts if c["type"] == "erc20"]
    for t in tokens:
        with Web3CliTest() as app:
            seed_chains(chains)
            app.set_args(
                [
                    "token",
                    "add",
                    t["name"],
                    t["address"],
                    "--desc",
                    t["desc"],
                    "--chain",
                    t["chain"],
                ]
            ).run()
            contract = Contract.get_by_name_and_chain(t["name"], t["chain"])
            assert contract.select().count() == 1
            assert Contract.name == t["name"]
            assert Contract.desc == t["desc"]
            assert Contract.type == t["type"]
            assert Contract.address == t["address"]


def test_token_delete(
    contracts: List[ContractFields], chains: List[ChainFields]
) -> None:
    for c in contracts:
        with Web3CliTest() as app:
            seed_chains(chains)
            seed_contracts(contracts)
            if c["type"] != "erc20":
                with pytest.raises(ContractNotFound):
                    app.set_args(
                        [
                            "token",
                            "delete",
                            c["name"],
                            "--chain",
                            c["chain"],
                        ]
                    ).run()
                continue
            app.set_args(
                [
                    "token",
                    "delete",
                    c["name"],
                    "--chain",
                    c["chain"],
                ]
            ).run()
            assert Contract.select().count() == len(contracts) - 1
            with pytest.raises(ContractNotFound):
                Contract.get_by_name_and_chain_or_raise(c["name"], c["chain"])
