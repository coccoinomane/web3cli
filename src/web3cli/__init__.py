from web3cli.core.models.address import Address


def resolve_address(address_or_label: str) -> str:
    return Address.resolve_address(address_or_label)
