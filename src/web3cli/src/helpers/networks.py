from typing import List
from xmlrpc.client import Boolean
from web3factory import networks
from web3factory.types import NetworkConfig


def get_supported_networks() -> List[NetworkConfig]:
    """Return list of supported networks"""
    return networks.supported_networks


def is_network_supported(network: str) -> bool:
    """Is the given network supported?"""
    return networks.is_network_supported(network)
