class Web3CliError(Exception):
    """Generic errors"""

    pass


class AddressNotFound(Web3CliError):
    """When an address label is not found in the database"""

    pass


class AddressIsInvalid(Web3CliError):
    """When an address 0x... is not in a valid EVM format"""

    pass


class AddressNotResolved(Web3CliError):
    """When a string cannot be resolved to a valid address"""

    pass
