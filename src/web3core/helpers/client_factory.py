from typing import Any, Type, Union

from web3.types import ABI
from web3client.base_client import BaseClient

from web3core.exceptions import Web3CoreError
from web3core.helpers.crypto import decrypt_string
from web3core.models.chain import Chain
from web3core.models.contract import Contract, ContractType
from web3core.models.signer import Signer
from web3core.types import Logger


def make_base_client(
    chain: Chain,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain.

    Pass chain=None to get a generic client, not bound to any chain."""
    if chain is None:
        return base(node_uri=None, **client_args)
    if node_uri is None:
        node_uri = chain.pick_rpc().url
    if logger:
        logger(f"Using chain {chain.name} with RPC {node_uri}")
    client = base(node_uri=node_uri, **client_args)
    client.chain_id = chain.chain_id
    client.tx_type = chain.tx_type
    middlewares = chain.middlewares.split(",") if chain.middlewares else []
    client.set_middlewares([Chain.parse_middleware(m) for m in middlewares])
    return client


def make_base_wallet(
    chain: Chain,
    signer: Union[Signer, str],
    password: bytes,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Return a brand new client configured for the given blockchain,
    with signing support.

    You need to provide the signer (either its name in the DB or an
    already initialized signer object) and a password to decrypt the
    signer's key.

    Pass chain=None to get a generic signer, not bound to any chain."""
    client = make_base_client(chain, node_uri, base, **client_args)
    if isinstance(signer, str):
        signer = Signer.get_by_name_or_raise(signer)
    if logger:
        logger(f"Using signer '{signer.name}' with address {signer.address}")
    client.set_account(decrypt_string(signer.key, password))
    return client


def make_contract_client(
    contract: Union[Contract, str],
    chain: Chain,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to read from the given smart contract.

    The contract ABI will be fetched from either the contract
    at db or, if not present, from the contract type"""
    client = make_base_client(chain, node_uri, base, logger, **client_args)
    if isinstance(contract, str):
        contract = Contract.get_by_name_and_chain_or_raise(contract, chain.name)
    client.set_contract(contract.address, contract.resolve_abi())
    return client


def make_contract_wallet(
    contract: Union[Contract, str],
    chain: Chain,
    signer: Union[Signer, str],
    password: bytes,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Client suitable to interact with the given smart contract.
    The contract ABI will be fetched from the contract's itself,
    if present, or from the contract's type, if not."""
    client = make_base_wallet(
        chain, signer, password, node_uri, base, logger, **client_args
    )
    if isinstance(contract, str):
        contract = Contract.get_by_name_and_chain_or_raise(contract, chain.name)
    client.set_contract(contract.address, contract.resolve_abi())
    return client


def make_contract_client_from_address_and_abi(
    address: str,
    chain: Chain,
    abi: ABI = None,
    type: str = None,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Wrapper to make_contract_client that returns a client
    even if the contract is not saved at database."""
    if (not abi and not type) or (abi and type):
        raise Web3CoreError(f"Please provide either the ABI or the contract type")
    if not abi:
        type_object = ContractType.get_by_name_or_raise(type)
        abi = type_object.abi
    contract = Contract(
        name=f"Contract at {address}",
        address=address,
        abi=abi,
        chain=chain.name,
    )
    return make_contract_client(contract, chain, node_uri, base, logger, **client_args)


def make_contract_wallet_from_address_and_abi(
    address: str,
    chain: Chain,
    signer: Union[Signer, str],
    password: bytes,
    abi: ABI = None,
    type: str = None,
    node_uri: str = None,
    base: Type[BaseClient] = BaseClient,
    logger: Logger = lambda msg: None,
    **client_args: Any,
) -> BaseClient:
    """Wrapper to make_contract_wallet that returns a client
    even if the contract is not saved at database."""
    if (not abi and not type) or (abi and type):
        raise Web3CoreError(f"Please provide either the ABI or the contract type")
    if not abi:
        type_object = ContractType.get_by_name_or_raise(type)
        abi = type_object.abi
    contract = Contract(
        name=f"Contract at {address}",
        address=address,
        abi=abi,
        chain=chain.name,
    )
    return make_contract_wallet(
        contract, chain, signer, password, node_uri, base, logger, **client_args
    )
