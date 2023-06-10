from urllib.parse import urlparse

from web3core.exceptions import Web3CoreError

HTTP_SCHEMES = {"http", "https"}
WS_SCHEMES = {"ws", "wss"}


def is_rpc_uri_valid(uri_string: str) -> bool:
    """Return True if the given string is a valid URI
    that can be used to access an RPC. Based on
    load_provider_from_uri() from Web3.py."""
    uri = urlparse(uri_string)
    if uri.scheme == "file":
        return True
    elif uri.scheme in HTTP_SCHEMES:
        return True
    elif uri.scheme in WS_SCHEMES:
        return True
    else:
        return False


def check_ws_or_raise(rpc_url: str) -> None:
    """Raise an error if the RPC URL is not a websocket or an IPC file"""
    if not rpc_url.startswith("ws") and not rpc_url.endswith(".ipc"):
        raise Web3CoreError("RPC must be a websocket URL or an IPC file")
