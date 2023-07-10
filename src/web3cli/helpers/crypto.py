import ast
import getpass
import json
from typing import Any

from eth_account import Account

from web3cli.exceptions import InvalidConfig, Web3CliError
from web3cli.framework.app import App
from web3core.helpers.crypto import decrypt_string, encrypt_string


def encrypt_string_with_app_key(app: App, message: str) -> bytes:
    """Encrypt a string message using the application key"""
    app_key = get_app_key_or_raise(app)
    return encrypt_string(message, app_key)


def decrypt_string_with_app_key(app: App, cypher: bytes) -> str:
    """Decrypt a cyphered message using the application key"""
    app_key = get_app_key_or_raise(app)
    return decrypt_string(cypher, app_key)


def get_app_key_or_raise(app: App) -> bytes:
    """Return the app key or raise an InvalidConfig exception
    if not found"""
    app_key = app.get_option("app_key")
    if not app_key:
        raise InvalidConfig(
            "Application key not defined; use `w3 app-key create` to generate one"
        )
    return ast.literal_eval(app_key)


def decrypt_keyfile(path: str) -> str:
    """Return the private key of the given keyfile file; the user will be asked
    for the password"""
    with open(path) as f:
        keyfile_dict = json.load(f)
    return decrypt_keyfile_dict(keyfile_dict)


def decrypt_keyfile_dict(keyfile_dict: dict[str, Any]) -> str:
    """Return the private key of the given keyfile dict; the user will be asked"""
    password = getpass.getpass("Keyfile password: ")
    try:
        private_key = Account.decrypt(keyfile_dict, password)
    except ValueError as e:
        raise Web3CliError(f"Could not decrypt keyfile: {e}")
    return private_key.hex().replace("0x", "")


def encrypt_to_keyfile(kdf: str = None, iterations: int = None) -> dict[str, Any]:
    """Return a keyfile dict obtained from the given private key; the
    user will be asked for the password"""
    private_key = getpass.getpass("Private key: ")
    password = getpass.getpass("Keyfile password: ")
    keyfile_dict = Account.encrypt(private_key, password, kdf, iterations)
    return keyfile_dict
