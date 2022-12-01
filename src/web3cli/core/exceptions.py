class Web3CliError(Exception):
    """Generic errors"""

    pass


class ChainNotFound(Web3CliError):
    """When a chain name is not found in the database"""

    pass


class AddressNotFound(Web3CliError):
    """When an address name is not found in the database"""

    pass


class AddressIsInvalid(Web3CliError):
    """When an address 0x... is not in a valid EVM format"""

    pass


class AddressNotResolved(Web3CliError):
    """When a string cannot be resolved to a valid address"""

    pass


class KeyIsInvalid(Web3CliError):
    """When a non-valid private key is provided"""

    pass


class RpcIsInvalid(Web3CliError):
    """When a non-valid RPC is used"""

    pass


class RpcNotFound(Web3CliError):
    """When an RPC cannot be found in the DB"""

    pass


class SignerNotFound(Web3CliError):
    """When a signer does not exist in the DB"""

    pass


class InvalidConfig(Web3CliError):
    """When any configuration value cannot be found"""

    pass


class TxNotFound(Web3CliError):
    """When a transaction hash is not found in the database"""

    pass


class TxIsInvalid(Web3CliError):
    """When a transatction hash is not in a valid EVM format"""

    pass
