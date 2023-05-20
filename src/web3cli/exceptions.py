class Web3CliError(Exception):
    """Generic CLI errors"""

    pass


class InvalidConfig(Web3CliError):
    """When any configuration value cannot be found"""

    pass


class SignerNotResolved(Web3CliError):
    """When a signer cannot be found (e.g. because it is not in the DB
    or the provided keyfile does not exist)"""

    pass
