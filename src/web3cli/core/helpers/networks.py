from typing import List
from web3factory import networks
from web3factory.types import NetworkConfig
from web3cli.core.models.chain import Chain


def get_supported_networks() -> List[NetworkConfig]:
    """Return list of supported networks"""
    return networks.supported_networks


def is_network_supported(network: str) -> bool:
    """Is the given network supported?"""
    return networks.is_network_supported(network)


def get_coin(network: str) -> str:
    """Return the ticker of the coin for the given network,
    e.g. ETH for ethereum, BNB for binance, etc."""
    return networks.get_network_config(network).get("coin")
