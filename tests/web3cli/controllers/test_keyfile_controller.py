from pathlib import Path
from typing import Any, Dict, List

import pytest

from tests.web3cli.main import Web3CliTest
from web3cli.helpers.crypto import decrypt_keyfile_dict


def test_keyfile_create(
    signers: List[Dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    for s in signers:
        with Web3CliTest() as app:
            # Create a keyfile JSON string from test signer private key
            responses = iter([s["private_key"], s["keyfile_password"]])
            monkeypatch.setattr("getpass.getpass", lambda _: next(responses))
            app.set_args(["keyfile", "create"]).run()
            data, output = app.last_rendered
            # Decrypt the keyfile to get again the private key
            keyfile_dict = data
            monkeypatch.setattr("getpass.getpass", lambda _: s["keyfile_password"])
            decoded_private_key = decrypt_keyfile_dict(keyfile_dict)
            # Test that the private key is the same
            assert decoded_private_key == s["private_key"]


def test_keyfile_decode(
    signers: List[Dict[str, Any]], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    for s in signers:
        # Create a keyfile from test signer
        f = tmp_path / f"keyfile_{s['name']}.json"
        f.write_text(s["keyfile"])
        keyfile = str(f)
        # Decode the keyfile
        with Web3CliTest() as app:
            responses = iter([s["keyfile_password"]])
            monkeypatch.setattr("getpass.getpass", lambda _: next(responses))
            app.set_args(["keyfile", "decrypt", keyfile]).run()
            data, output = app.last_rendered
            assert data == s["private_key"]
