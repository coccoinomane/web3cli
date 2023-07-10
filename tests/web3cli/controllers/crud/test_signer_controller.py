from typing import Any, Dict, List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.exceptions import SignerNotResolved
from web3cli.helpers.crypto import decrypt_string_with_app_key
from web3cli.helpers.database import truncate_tables
from web3core.exceptions import RecordNotFound
from web3core.helpers.seed import seed_signers
from web3core.models.signer import Signer


def test_signer_list(signers: List[Dict[str, Any]]) -> None:
    """Add signers and check that they are listed alphabetically"""

    signers = sorted(signers, key=lambda s: s["name"])
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        app.set_args(["signer", "list"]).run()
        data, output = app.last_rendered
        for i in range(0, len(signers)):
            assert data[i][0] == signers[i]["name"]


def test_signer_get(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(signers, app.app_key)
            app.set_args(
                [
                    "signer",
                    "get",
                    s["name"],
                ]
            ).run()
            data, output = app.last_rendered
            assert data["name"] == s["name"]
            assert data["address"] == s["address"]
            assert data["key"] == "********"


# Test with --signer argument > returns address of signer
def test_signer_active(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            seed_signers(signers, app.app_key)
            app.set_args(["signer", "active", "--signer", s["name"]]).run()
            data, output = app.last_rendered
            assert data == s["address"]


# Test without arguments > returns whatever is written in config file
def test_signer_active_with_default_signer(signers: List[Dict[str, Any]]) -> None:
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        app.set_option("default_signer", s["name"])
        app.set_args(["signer", "active"]).run()
        data, output = app.last_rendered
        assert data == s["address"]


# Test without arguments, without config file, but there's one signer in the DB > returns that one signer
def test_signer_active_with_one_signer(signers: List[Dict[str, Any]]) -> None:
    s = signers[0]
    with Web3CliTest() as app:
        seed_signers([s], app.app_key)
        app.set_args(["signer", "active"]).run()
        data, output = app.last_rendered
        assert data == s["address"]


# Test without arguments, without config file, but there are multiple signers in the DB > raise error
def test_signer_active_with_multiple_signers(signers: List[Dict[str, Any]]) -> None:
    with Web3CliTest() as app:
        seed_signers(signers, app.app_key)
        with pytest.raises(SignerNotResolved):
            app.set_args(["signer", "active"]).run()


# Test without arguments, without config file, without signers in the DB > raise error
def test_signer_active_with_no_signers(signers: List[Dict[str, Any]]) -> None:
    with Web3CliTest() as app:
        with pytest.raises(SignerNotResolved):
            app.set_args(["signer", "active"]).run()


def test_signer_add(signers: List[Dict[str, Any]]) -> None:
    for s in signers:
        with Web3CliTest() as app:
            app.set_args(
                [
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
    """Test `w3 signer add <name> --create`"""
    names = ["name_1", "name_2", "name_3"]
    for i, s_name in enumerate(names):
        with Web3CliTest(delete_db=False) as app:
            if i == 0:
                truncate_tables(app)
            app.set_args(
                [
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
                    "signer",
                    "delete",
                    s["name"],
                ]
            ).run()
            assert Signer.select().count() == len(signers) - 1
            with pytest.raises(RecordNotFound):
                Signer.get_by_name_or_raise(s["name"])
