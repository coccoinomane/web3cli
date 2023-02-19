import time

from web3.contract import ContractFunction
from web3.exceptions import TransactionNotFound
from web3.types import Nonce, TxData, Wei
from web3client.base_client import BaseClient

from web3core.types import TxLife


def send_contract_transaction(
    client: BaseClient,
    function: ContractFunction,
    dry_run: bool = False,
    call: bool = False,
    fetch_data: bool = False,
    fetch_receipt: bool = False,
    from_address: str = None,
    valueInWei: Wei = None,
    nonce: Nonce = None,
    gasLimit: int = None,
    maxPriorityFeePerGasInGwei: int = None,
) -> TxLife:
    """Shortcut to send a transaction to a contract function, printing the
    output according to the output_type parameter.

    ARGUMENTS
    ---------
    - client (BaseClient): The client to use to send the transaction.
    - function (ContractFunction): The function to call.
    - dry_run (bool): If True, the transaction will not be sent to the
      blockchain.
    - call (bool): If True, the contract function will be called with eth_call before
      sending the transaction. This is useful to check if the transaction
      will fail for any reason (e.g. insufficient gas) before sending it.
      Please note that if you use --no-call you also need to provide a gasLimit,
      lest web3.py will try to estimate the gas limit on-chain which another
      function call.
    - fetch_data (bool): If True, fetch the transaction data after sending the
      tx, and include it in the output. Ignored if dry_run is True.
    - fetch_receipt (bool): If True, fetch the receipt after sending the tx,
      and include it in the output. This will wait for the transaction to
      be mined. Ignored if dry_run is True.
    - from_address (str): The address to use as the sender of the transaction.
      If not provided, the signer's address in the client will be used.
    - valueInWei (Wei): The value to send with the transaction.
    - nonce (Nonce): The nonce to use for the transaction.
    - gasLimit (int): The gas limit to use for the transaction.
    - maxPriorityFeePerGasInGwei (int): The max priority fee per gas to use
      for the transaction.

    RETURNS
    -------
    TxLife: The transaction life cycle, as a dictionary with the following
    keys:

    - params: The transaction parameters.
    - hash: The transaction hash.
    - sig: The signed transaction.
    - function_output: The output of the contract function, if
    call is True.
    - data: The transaction data, if fetch_data is True.
    - receipt: The transaction receipt, if fetch_receipt is True.
    """
    # Prepare output
    tx_life: TxLife = {
        "hash": None,
        "params": None,
        "sig": None,
        "output": None,
        "data": None,
        "receipt": None,
    }
    # Build transaction
    tx_life["params"] = client.buildContractTransaction(
        function,
        valueInWei=valueInWei,
        nonce=nonce,
        gasLimit=gasLimit,
        maxPriorityFeePerGasInGwei=maxPriorityFeePerGasInGwei,
    )
    # Sign transaction
    signed_tx = client.signTransaction(tx_life["params"])
    tx_life["sig"] = signed_tx._asdict()
    # Call function
    if call:
        tx_life["output"] = function.call({"from": from_address or client.userAddress})
    # Send transaction
    if not dry_run:
        tx_life["hash"] = client.sendSignedTransaction(signed_tx)
        if fetch_data:
            tx_life["data"] = poll_transaction(client, tx_life["hash"])
        if fetch_receipt:
            tx_life["receipt"] = client.getTransactionReceipt(tx_life["hash"])
    else:
        tx_life["hash"] = signed_tx.hash.hex()
    return tx_life


def poll_transaction(
    client: BaseClient, tx_hash: str, poll_interval: int = 1, poll_timeout: int = 30
) -> TxData:
    """Get a transaction from the blockchain. If the transaction is not
    found, poll until it is found. If it is not found after poll_timeout
    seconds, return None.

    ARGUMENTS
    ---------
    - client (BaseClient): The client to use to send the transaction.
    - tx_hash (str): The transaction hash.
    - poll_interval (int): The number of seconds to wait between polls. Set
      to None to disable polling.
    - poll_timeout (int): The number of seconds to wait before timing out,
      and returning None. Set to None to wait indefinitely. Set to zero
      to disable polling.

    RETURNS
    -------
    TxData: The transaction data.
    """
    if poll_interval is None:
        return client.getTransaction(tx_hash)

    start_time = time.time()
    while True:
        try:
            return client.getTransaction(tx_hash)
        except TransactionNotFound:
            time.sleep(poll_interval)
            if time.time() - start_time > poll_timeout:
                return None
