import asyncio
from typing import Any, Dict

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client
from web3cli.helpers.render import render_web3py
from web3core.helpers.rpc import check_ws_or_raise


class SubscribeController(Controller):
    """Handler of the `w3 subscribe` commands"""

    class Meta:
        label = "subscribe"
        help = "Subscribe to stuff happening on the blockchain. Requires a websocket connection.  Please note that not all chains support subscriptions (eth_subscribe)."
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Print to screen new blocks as they are mined (newHeads subscription)",
        arguments=[*args.chain_and_rpc()],
    )
    def blocks(self) -> None:
        """Print to screen new blocks as they are mined"""
        check_ws_or_raise(self.app.rpc.url)

        async def callback(block: Dict[str, Any]) -> None:
            render_web3py(self.app, block)

        asyncio.run(
            make_client(self.app).async_subscribe(
                on_notification=callback, subscription_type="newHeads"
            )
        )
