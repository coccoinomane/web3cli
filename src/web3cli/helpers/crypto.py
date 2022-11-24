from cement import App
from web3cli.core.exceptions import InvalidConfig
from web3cli.core.helpers.crypto import encrypt_string, decrypt_string
import ast


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
    app_key = app.config.get("web3cli", "app_key")
    if not app_key:
        raise InvalidConfig(
            "Application key not defined; use `w3 key create` to generate one"
        )
    return ast.literal_eval(app_key)
