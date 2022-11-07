import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(message: bytes, key: bytes) -> bytes:
    """Encrypt a message using AES256-GCM. Requires a 32 bytes key, e.g.
    secrets.token_bytes(32)
    Source: https://stackoverflow.com/a/59835994/2972183"""
    nonce = secrets.token_bytes(12)  # GCM mode needs 12 fresh bytes every time
    return nonce + AESGCM(key).encrypt(nonce, message, b"")


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt from AES256-GCM encryption. Raises InvalidTag if
    using wrong key or corrupted ciphertext
    Source: https://stackoverflow.com/a/59835994/2972183"""
    return AESGCM(key).decrypt(ciphertext[:12], ciphertext[12:], b"")
