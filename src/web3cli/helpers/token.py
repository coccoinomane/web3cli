from typing import Any

from web3client.base_client import BaseClient

from web3cli.framework.app import App
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers.resolve import resolve_address


def approve(
    app: App,
    token_client: BaseClient,
    spender: str,
    amount_in_wei: int = None,
    check_allowance: bool = True,
    **send_contract_tx_kwargs: Any,
) -> None:
    """Approve a spender to spend your token balance.
    By default, allow to spend an infinite amount of tokens."""

    # Approve an infinite amount of tokens unless amount is provided
    if amount_in_wei == None:
        amount_in_wei = 2**256 - 1

    # Spender can be a tag
    spender = resolve_address(spender)

    # If allowance is sufficient, do nothing
    if check_allowance:
        allowance = token_client.functions["allowance"](
            token_client.user_address, spender
        ).call()
        if allowance >= amount_in_wei:
            return

    app.pargs._return = "hash"  # return tx hash
    return send_contract_tx(
        app=app,
        client=token_client,
        function=token_client.functions["approve"](spender, amount_in_wei),
        tx_return_dest="_return",
        **({"fetch_receipt": True} | send_contract_tx_kwargs),
    )


def revoke(
    app: App, token_client: BaseClient, spender: str, **send_contract_tx_kwargs: Any
) -> None:
    """Revoke token spending permissions from the given spender"""
    return approve(
        app, token_client, spender, 0, check_allowance=False, **send_contract_tx_kwargs
    )
