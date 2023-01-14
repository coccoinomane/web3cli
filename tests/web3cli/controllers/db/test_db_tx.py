from typing import List

import pytest

from tests.web3cli.main import Web3CliTest
from web3core.exceptions import TxNotFound
from web3core.helpers.seed import seed_txs
from web3core.models.tx import Tx
from web3core.models.types import TxFields


def test_tx_list(txs: List[TxFields]) -> None:
    """Add txs and check that they are listed from oldest to newest"""
    txs = sorted(txs, key=lambda t: t["created_at"], reverse=True)
    with Web3CliTest() as app:
        seed_txs(txs)
        app.set_args(["db", "trx", "list"]).run()
        data, output = app.last_rendered
        for i in range(0, len(txs)):
            assert data[i][0] == txs[i]["hash"]
            assert data[i][1] == str(txs[i]["chain"])


def test_tx_get(txs: List[TxFields]) -> None:
    for t in txs:
        with Web3CliTest() as app:
            seed_txs(txs)
            app.set_args(
                [
                    "db",
                    "trx",
                    "get",
                    t["hash"],
                ]
            ).run()
            data, output = app.last_rendered
            assert t["hash"] in output
            assert str(t["gas"]) in output
            assert t["gas_price"] in output


def test_tx_add(txs: List[TxFields]) -> None:
    for t in txs:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "db",
                    "trx",
                    "add",
                    t["hash"],
                    t["from_"],
                    t["to"],
                ]
            ).run()
            tx = Tx.get_by_hash(t["hash"])
            assert tx.select().count() == 1
            assert Tx.from_ == t["from_"]
            assert Tx.to == t["to"]


def test_tx_update(txs: List[TxFields]) -> None:
    """Create tx 0, then update it with the data of tx 1,
    while keeping the same hash"""
    with Web3CliTest() as app:
        seed_txs([txs[0]])
        app.set_args(
            argv=[
                "db",
                "trx",
                "add",
                txs[0]["hash"],
                txs[1]["from_"],
                txs[1]["to"],
                "--update",
            ]
        ).run()
        tx = Tx.get_by_hash(txs[0]["hash"])
        assert Tx.from_ == txs[1]["from_"]
        assert Tx.to == txs[1]["to"]


def test_tx_delete(txs: List[TxFields]) -> None:
    for t in txs:
        with Web3CliTest() as app:
            seed_txs(txs)
            app.set_args(
                [
                    "db",
                    "trx",
                    "delete",
                    t["hash"],
                ]
            ).run()
            assert Tx.select().count() == len(txs) - 1
            with pytest.raises(TxNotFound):
                Tx.get_by_hash_or_raise(t["hash"])
