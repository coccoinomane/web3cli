from typing import Any

from web3.contract.contract import ContractFunction
from web3.types import Nonce, Wei
from web3client.base_client import BaseClient

from web3cli.framework.app import App
from web3cli.helpers import args
from web3core.helpers.tx import send_contract_tx as _send_contract_tx


def send_contract_tx(
    app: App,
    client: BaseClient,
    function: ContractFunction,
    value_in_wei: Wei = None,
    nonce: Nonce = None,
    dry_run_dest: str = "dry_run",
    tx_return_dest: str = "return",
    tx_call_dest: str = "call",
    tx_gas_limit_dest: str = "gas_limit",
    **kwargs: Any,
) -> Any:
    """Send a transaction to a contract function, and return the
    output according to the output_type parameter.

    This is a wrapper around web3core's send_contract_tx
    that prefills some of the arguments from the CLI and the app."""
    # Parse tx-related arguments
    dry_run, tx_return, tx_call, tx_gas_limit = args.parse_tx_args(
        app, dry_run_dest, tx_return_dest, tx_call_dest, tx_gas_limit_dest
    )
    # Build args
    fixed_args = {
        "client": client,
        "function": function,
        "dry_run": dry_run,
        "value_in_wei": value_in_wei,
        "nonce": nonce,
    }
    extra_args = {
        "call": tx_call,
        "fetch_data": True if tx_return in ["data", "all"] else False,
        "fetch_receipt": True if tx_return in ["receipt", "all"] else False,
        "from_address": client.user_address,
        "gas_limit": tx_gas_limit,
        "max_priority_fee_in_gwei": app.priority_fee,
    } | kwargs
    # Inform user
    app.log.debug(
        f"Sending tx '{function.fn_name}' [dry_run={dry_run}, value={value_in_wei}, nonce={nonce}, extra_args={extra_args}]..."
    )
    # Send transaction
    tx_life = _send_contract_tx(**(fixed_args | extra_args))
    # Return tx details according to tx_return
    if tx_return == "all":
        return tx_life
    else:
        return tx_life[tx_return]
