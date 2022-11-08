from cement import App
from web3cli.core.exceptions import InvalidConfig
from web3cli.core.helpers.crypto import encrypt, decrypt
from base64 import b64encode, b64decode
import ast


def encrypt_with_app_key(app: App, message: str) -> bytes:
    """Encrypt a message using the given key"""
    app_key = get_app_key_or_raise(app)
    return encrypt(message.encode("utf-8"), app_key)


def decrypt_with_app_key(app: App, cypher: bytes) -> str:
    """Decrypt a cyphered message using the given key"""
    app_key = get_app_key_or_raise(app)
    return decrypt(cypher, app_key).decode("utf-8")


def get_app_key_or_raise(app: App) -> bytes:
    """Return the app key or raise an InvalidConfig exception
    if not found"""
    app_key = app.config.get("web3cli", "app_key")
    if not app_key:
        raise InvalidConfig(
            "Application key not defined; use `web3 key create` to generate one"
        )
    return ast.literal_eval(app_key)
