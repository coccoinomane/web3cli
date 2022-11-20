from urllib.parse import urlparse


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
