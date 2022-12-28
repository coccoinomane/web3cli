class Web3CliError(Exception):
    """Generic CLI errors"""

    pass


class InvalidConfig(Web3CliError):
    """When any configuration value cannot be found"""

    pass
