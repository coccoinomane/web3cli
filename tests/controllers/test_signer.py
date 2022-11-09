from typing import Any, List, Dict
from ..main import Web3CliTest
from web3cli.core.models.signer import Signer
from eth_account import Account
from web3cli.helpers.crypto import decrypt_string_with_app_key


def test_signer_list(signers: List[Dict[str, Any]]) -> None:
    """Add signers and check that they are listed alphabetically"""

    signers = sorted(signers, key=lambda s: s["label"])
    argv = ["signer", "list"]
    with Web3CliTest(argv=argv) as app:
        for s in signers:
            address = Account.from_key(s["private_key"]).address
            Signer.create(label=s["label"], address=address, key=s["private_key"])
        app.run()
        data, output = app.last_rendered
        for i in range(0, len(signers)):
            assert data[i][0] == signers[i]["label"]


def test_signer_get(signers: List[Dict[str, Any]]) -> None:
    # Test with label argument > returns address of signer with label
    for s in signers:
        argv = [
            "signer",
            "get",
            s["label"],
        ]
        with Web3CliTest(argv=argv) as app:
            address = Account.from_key(s["private_key"]).address
            Signer.create(label=s["label"], address=address, key=s["private_key"])
            app.run()
            data, output = app.last_rendered
            assert data["out"] == s["address"]

    # Test with --signer argument > returns value of argument
    for s in signers:
        argv = [
            "--signer",
            s["label"],
            "signer",
            "get",
        ]
        with Web3CliTest(argv=argv) as app:
            address = Account.from_key(s["private_key"]).address
            Signer.create(label=s["label"], address=address, key=s["private_key"])
            app.run()
            data, output = app.last_rendered
            assert data["out"] == s["label"]

    # Test without arguments > returns whatever is written in config file
    s = signers[0]
    argv = [
        "signer",
        "get",
    ]
    with Web3CliTest(argv=argv) as app:
        app.config.set("web3cli", "default_signer", s["label"])
        address = Account.from_key(s["private_key"]).address
        Signer.create(label=s["label"], address=address, key=s["private_key"])
        app.run()
        data, output = app.last_rendered
        assert data["out"] == s["label"]


def test_signer_add(signers: List[Dict[str, Any]], app_key: str) -> None:
    for s in signers:
        argv = [
            "signer",
            "add",
            s["label"],
            "--private-key",
            s["private_key"],
        ]
        with Web3CliTest(argv=argv) as app:
            app.config.set("web3cli", "app_key", str(app_key))
            app.run()
            signer = Signer.get_by_label(s["label"])
            assert Signer.select().count() == 1
            assert signer.address == s["address"]
            assert decrypt_string_with_app_key(app, signer.key) == s["private_key"]


def test_signer_delete(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        argv = [
            "signer",
            "delete",
            s["label"],
        ]
        with Web3CliTest(argv=argv) as app:
            address = Account.from_key(s["private_key"]).address
            Signer.create(label=s["label"], address=address, key=s["private_key"])
            app.run()
            assert Signer.select().count() == 0
