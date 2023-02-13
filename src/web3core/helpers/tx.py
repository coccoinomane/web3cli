from typing import Any

from web3.contract import ContractFunction
from web3.types import Nonce, Wei
from web3client.base_client import BaseClient

from web3core.exceptions import Web3CoreError


def send_contract_transaction(
    client: BaseClient,
    function: ContractFunction,
    dry_run: bool,
    output_type: str,
    valueInWei: Wei = None,
    nonce: Nonce = None,
    gasLimit: int = None,
    maxPriorityFeePerGasInGwei: int = None,
) -> Any:
    # Build transaction
    tx = client.buildContractTransaction(
        function,
        valueInWei=valueInWei,
        nonce=nonce,
        gasLimit=gasLimit,
        maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
    )
    # Sign transaction
    tx_signed = client.signTransaction(tx)
    # Send transaction
    if not dry_run:
        tx_hash = client.sendSignedTransaction(tx_signed)
    else:
        tx_hash = tx_signed.hash.hex()
    # Print output
    if output_type == "hash":
        return tx_hash
    elif output_type == "tx":
        return tx
    elif output_type == "sig":
        return tx_signed._asdict()
    elif output_type == "call":
        return function.call()
    elif output_type in ["receipt", "rcpt"]:
        rcpt = client.getTransactionReceipt(tx_hash)
        return rcpt
    else:
        raise Web3CoreError(f"Unknown output type: {output_type}")
