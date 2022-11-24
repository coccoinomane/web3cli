import random
from typing import Any, List, Dict
from tests.helper import get_random_string
from tests.seeder import seed_signers
from tests.main import Web3CliTest
from web3cli.core.exceptions import SignerNotFound
from web3cli.core.models.signer import Signer
from web3cli.helpers.crypto import decrypt_string_with_app_key
import pytest
from web3cli.helpers.database import delete_db_file, truncate_tables


def test_signer_list(signers: List[Dict[str, Any]]) -> None:
    """Add signers and check that they are listed alphabetically"""

    signers = sorted(signers, key=lambda s: s["label"])
    with Web3CliTest() as app:
        seed_signers(app, signers)
        app.set_args(["signer", "list"]).run()
        data, output = app.last_rendered
        for i in range(0, len(signers)):
            assert data[i][0] == signers[i]["label"]


def test_signer_get(signers: List[Dict[str, Any]]) -> None:
    # Test with label argument > returns address of signer with label
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(app, signers)
            app.set_args(
                [
                    "signer",
                    "get",
                    s["label"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == s["address"]

    # Test with --signer argument > returns value of argument
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(app, signers)
            app.set_args(
                [
                    "--signer",
                    s["label"],
                    "signer",
                    "get",
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == s["label"]

    # Test without arguments > returns whatever is written in config file
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers(app, signers)
        app.config.set("web3cli", "default_signer", s["label"])
        app.set_args(
            [
                "signer",
                "get",
            ]
        ).run()
        data, output = app.last_rendered
        assert data["out"] == s["label"]

    # Test without arguments, without config file, but there's one signer in the DB > returns that one signer
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers(app, [s])
        app.set_args(
            [
                "signer",
                "get",
            ]
        ).run()
        data, output = app.last_rendered
        assert data["out"] == s["label"]

    # Test without arguments, without config file, but there are multiple signers in the DB > raise error
    with Web3CliTest() as app:
        seed_signers(app, signers)
        with pytest.raises(SignerNotFound):
            app.set_args(
                [
                    "signer",
                    "get",
                ]
            ).run()

    # Test without arguments, without config file, without signers in the DB > raise error
    s = signers[0]
    with Web3CliTest() as app:
        with pytest.raises(SignerNotFound):
            app.set_args(
                [
                    "signer",
                    "get",
                ]
            ).run()


def test_signer_add(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        argv = [
            "signer",
            "add",
            s["label"],
            "--private-key",
            s["private_key"],
        ]
        with Web3CliTest(argv=argv) as app:
            app.run()
            signer = Signer.get_by_label(s["label"])
            assert Signer.select().count() == 1
            assert signer.address == s["address"]
            assert decrypt_string_with_app_key(app, signer.key) == s["private_key"]


def test_signer_add_create(signers: List[Dict[str, Any]]) -> None:
    """Test `w3 signer add <label> --create`"""
    labels = ["label_1", "label_2", "label_3"]
    for i, s_label in enumerate(labels):
        with Web3CliTest(delete_db=False) as app:
            i == 0 and truncate_tables(app)
            app.set_args(
                [
                    "signer",
                    "add",
                    s_label,
                    "--create",
                ]
            ).run()
            assert Signer.select().count() == i + 1


def test_signer_delete(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(app, signers)
            app.set_args(
                [
                    "signer",
                    "delete",
                    s["label"],
                ]
            ).run()
            assert Signer.select().count() == len(signers) - 1
