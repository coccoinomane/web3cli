class Web3CliError(Exception):
    """Generic errors"""

    pass


class AddressNotFound(Web3CliError):
    """When an address is not found from the database"""

    pass
