import web3


def is_valid_address(address: str) -> bool:
    return web3.main.is_address(address)
