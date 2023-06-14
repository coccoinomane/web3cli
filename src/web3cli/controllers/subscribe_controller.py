import asyncio
import json
from typing import Any, Awaitable, Callable

import requests
from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client
from web3cli.helpers.render import render
from web3cli.helpers.telegram import send_tg_message
from web3core.helpers.resolve import resolve_address
from web3core.helpers.rpc import check_ws_or_raise
from web3core.helpers.validation import is_valid_url


class SubscribeController(Controller):
    """Handler of the `w3 subscribe` commands"""

    class Meta:
        label = "subscribe"
        help = "Subscribe to stuff happening on the blockchain. Requires a websocket connection.  It uses the 'eth_subscribe' RPC method, which is not supported by all chains and nodes.  More details here > https://geth.ethereum.org/docs/interacting-with-geth/rpc/pubsub"
        stacked_type = "nested"
        stacked_on = "base"
        aliases = ["sub"]

    @ex(
        help="Show new blocks as they are mined.  Uses the 'newHeads' subscription.",
        arguments=[*args.subscribe_actions(), *args.chain_and_rpc()],
        aliases=["block", "headers"],
    )
    def blocks(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        self.app.log.info("Subscribing to new blocks, press Ctrl+C to stop...")
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.get_callback(),
                subscription_type="newHeads",
            )
        )

    @ex(
        help="Show new transactions before they are mined.  Uses the 'newPendingTransactions' subscription, which is supported only by chains with a mempool.",
        arguments=[
            args.subscribe_senders(),
            *args.subscribe_actions(),
            *args.chain_and_rpc(),
        ],
        aliases=["pending_txs", "txs"],
    )
    def pending(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        self.app.log.info(
            "Subscribing to new pending transactions, press Ctrl+C to stop..."
        )
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.get_callback(),
                subscription_type="newPendingTransactions",
                tx_from=[
                    resolve_address(a, chain=self.app.chain.name)
                    for a in self.app.pargs.senders
                ],
                tx_on_fetch_error=lambda e, data: self.app.log.warning(e),
            )
        )

    @ex(
        help="Show contract events as they are emitted.  Uses the 'logs' subscription.",
        arguments=[
            (
                ["--contracts"],
                {
                    "help": "Consider only events emitted by these smart contracts",
                    "nargs": "+",
                    "default": [],
                },
            ),
            (
                ["--topics"],
                {
                    "help": "Consider only events with these topics",
                    "nargs": "+",
                    "default": [],
                },
            ),
            args.subscribe_senders(),
            *args.subscribe_actions(),
            *args.chain_and_rpc(),
        ],
        aliases=["logs"],
    )
    def events(self) -> None:
        check_ws_or_raise(self.app.rpc.url)
        self.app.log.info("Subscribing to new events, press Ctrl+C to stop...")
        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=self.get_callback(),
                subscription_type="logs",
                logs_addresses=[
                    resolve_address(a, chain=self.app.chain.name)
                    for a in self.app.pargs.contracts
                ],
                logs_topics=self.app.pargs.topics,
                tx_from=[
                    resolve_address(a, chain=self.app.chain.name)
                    for a in self.app.pargs.senders
                ],
                tx_on_fetch_error=lambda e, data: self.app.log.warning(e),
            )
        )

    def get_callback(self) -> Callable[[Any], Awaitable[None]]:
        """Return the callback to invoke when a notification is received,
        based on the command arguments."""

        async def callback(data: Any) -> None:
            # PRINT CALLBACK
            if self.app.pargs.print:
                render(self.app, data)
            # TELEGRAM CALLBACK
            if self.app.pargs.telegram:
                send_tg_message(
                    self.app,
                    body=json.dumps(data, indent=4),
                    chat_id=self.app.pargs.telegram
                    if self.app.pargs.telegram != "config"
                    else None,
                )
            # POST CALLBACK
            if self.app.pargs.post:
                url = self.app.pargs.post[0]
                if not is_valid_url(url):
                    raise Web3CliError(f"Invalid URL: {url}")
                requests.post(
                    url=url,
                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"},
                    timeout=self.app.config.get("web3cli", "post_callback_timeout"),
                )

        return callback
