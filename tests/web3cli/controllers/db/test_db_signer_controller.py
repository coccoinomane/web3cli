from typing import Any, Dict, List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.helpers.crypto import decrypt_string_with_app_key
from web3cli.helpers.database import truncate_tables
from web3core.exceptions import RecordNotFound, SignerNotFound
from web3core.helpers.seed import seed_signers
from web3core.models.signer import Signer


def test_signer_list(signers: List[Dict[str, Any]]) -> None:
    """Add signers and check that they are listed alphabetically"""

    signers = sorted(signers, key=lambda s: s["name"])
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        app.set_args(["db", "signer", "list"]).run()
        data, output = app.last_rendered
        for i in range(0, len(signers)):
            assert data[i][0] == signers[i]["name"]


def test_signer_get(signers: List[Dict[str, Any]]) -> None:
    # Test with name argument > returns address of signer with name
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(signers, app.app_key)
            app.set_args(
                [
                    "db",
                    "signer",
                    "get",
                    s["name"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == s["address"]

    # Test with --signer argument > returns value of argument
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(signers, app.app_key)
            app.set_args(
                [
                    "--signer",
                    s["name"],
                    "db",
                    "signer",
                    "get",
                ]
            ).run()
            data, output = app.last_rendered
            assert data["out"] == s["name"]

    # Test without arguments > returns whatever is written in config file
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        app.config.set("web3cli", "default_signer", s["name"])
        app.set_args(
            [
                "db",
                "signer",
                "get",
            ]
        ).run()
        data, output = app.last_rendered
        assert data["out"] == s["name"]

    # Test without arguments, without config file, but there's one signer in the DB > returns that one signer
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers([s], app.app_key)
        app.set_args(
            [
                "db",
                "signer",
                "get",
            ]
        ).run()
        data, output = app.last_rendered
        assert data["out"] == s["name"]

    # Test without arguments, without config file, but there are multiple signers in the DB > raise error
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        with pytest.raises(SignerNotFound):
            app.set_args(
                [
                    "db",
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
                    "db",
                    "signer",
                    "get",
                ]
            ).run()


def test_signer_add(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "db",
                    "signer",
                    "add",
                    s["name"],
                    "--private-key",
                    s["private_key"],
                ]
            ).run()
            signer = Signer.get_by_name(s["name"])
            assert Signer.select().count() == 1
            assert signer.address == s["address"]
            assert decrypt_string_with_app_key(app, signer.key) == s["private_key"]


def test_signer_add_create(signers: List[Dict[str, Any]]) -> None:
    """Test `w3 db signer add <name> --create`"""
    names = ["name_1", "name_2", "name_3"]
    for i, s_name in enumerate(names):
        with Web3CliTest(delete_db=False) as app:
            if i == 0:
                truncate_tables(app)
            app.set_args(
                [
                    "db",
                    "signer",
                    "add",
                    s_name,
                    "--create",
                ]
            ).run()
            assert Signer.select().count() == i + 1


def test_signer_delete(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(signers, app.app_key)
            app.set_args(
                [
                    "db",
                    "signer",
                    "delete",
                    s["name"],
                ]
            ).run()
            assert Signer.select().count() == len(signers) - 1
            with pytest.raises(RecordNotFound):
                Signer.get_by_name_or_raise(s["name"])
