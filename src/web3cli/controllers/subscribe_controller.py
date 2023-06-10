import asyncio
from typing import Any, Awaitable, Callable

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client
from web3cli.helpers.render import render
from web3core.helpers.resolve import resolve_address
from web3core.helpers.rpc import check_ws_or_raise


class SubscribeController(Controller):
    """Handler of the `w3 subscribe` commands"""

    class Meta:
        label = "subscribe"
        help = "Subscribe to stuff happening on the blockchain. Requires a websocket connection.  It uses the 'eth_subscribe' RPC method, which is not supported by all chains and nodes.  More details here > https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Show new blocks as they are mined.  Uses the 'newHeads' subscription.",
        arguments=[args.callback(), *args.chain_and_rpc()],
        aliases=["block", "headers"],
    )
    def blocks(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.resolve_callback(self.app.pargs.callback),
                subscription_type="newHeads",
            )
        )

    @ex(
        help="Show new transactions before they are mined.  Uses the 'newPendingTransactions' subscription, which is supported only by chains with a mempool.",
        arguments=[args.callback(), *args.chain_and_rpc()],
        aliases=["pending_txs", "txs"],
    )
    def pending(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.resolve_callback(self.app.pargs.callback),
                subscription_type="newPendingTransactions",
            )
        )

    @ex(
        help="Show contact events as they are emitted.  Uses the 'logs' subscription.",
        arguments=[
            (
                ["--addresses"],
                {
                    "help": "only show events from these addresses",
                    "nargs": "+",
                    "type": str,
                    "default": [],
                },
            ),
            (
                ["--topics"],
                {
                    "help": "only show events with these topics",
                    "nargs": "+",
                    "type": str,
                    "default": [],
                },
            ),
            args.callback(),
            *args.chain_and_rpc(),
        ],
        aliases=["logs"],
    )
    def events(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.resolve_callback(self.app.pargs.callback),
                subscription_type="logs",
                logs_addresses=[
                    resolve_address(a, chain=self.app.chain.name)
                    for a in self.app.pargs.addresses
                ],
                logs_topics=self.app.pargs.topics,
            )
        )

    def resolve_callback(self, callback: str) -> Callable[[Any], Awaitable[None]]:
        """Get a callback function by its name.
        TODO: Replace with a class, where each subclass is a callback type."""
        if callback == "print":
            return self.callback_print
        elif callback in ["store", "post", "telegram", "email"]:
            raise NotImplementedError(f"Callback {callback} not implemented yet")
        else:
            raise Web3CliError(f"Unknown callback: {callback}")

    async def callback_print(self, data: Any) -> None:
        """Print whatever comes from the subscription"""
        render(self.app, data)
