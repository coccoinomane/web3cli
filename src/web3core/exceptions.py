class Web3CoreError(Exception):
    """Generic errors"""

    pass


class NotSupportedYet(Web3CoreError):
    """When a feature is not supported yet"""

    pass


class RecordNotFound(Web3CoreError):
    """When a record from the database is not found"""

    pass


class ChainNotFound(RecordNotFound):
    """When a chain name is not found in the database"""

    pass


class ChainNotResolved(Web3CoreError):
    """When a string cannot be resolved to a chain"""

    pass


class AddressIsInvalid(Web3CoreError):
    """When an address 0x... is not in a valid EVM format"""

    pass


class AddressNotResolved(Web3CoreError):
    """When a string cannot be resolved to a valid address"""

    pass


class KeyIsInvalid(Web3CoreError):
    """When a non-valid private key is provided"""

    pass


class RpcIsInvalid(Web3CoreError):
    """When a non-valid RPC is used"""

    pass


class RpcNotFound(RecordNotFound):
    """When an RPC cannot be found in the DB"""

    pass


class SignerNotFound(RecordNotFound):
    """When a signer does not exist in the DB"""

    pass


class TxNotFound(Web3CoreError):
    """When a transaction hash is not found in the database"""

    pass


class TxIsInvalid(Web3CoreError):
    """When a transatction hash is not in a valid EVM format"""

    pass


class ContractNotFound(RecordNotFound):
    """When a contract name is not found in the database"""

    pass


class ContractIsInvalid(Web3CoreError):
    """When a contract address or other field is not valid
    EVM format"""

    pass


class ContractAbiNotResolved(Web3CoreError):
    """When the ABI of a contract cannot be found"""

    pass


class AbiOverflow(Web3CoreError):
    """When you pass an int or unit too big for the ABI type"""

    pass
