import asyncio
from typing import Any

from cement import ex
from web3 import exceptions as web3_exceptions
from web3.types import TxData
from web3client.types import AsyncSubscriptionCallback, SubscriptionType

from web3cli.controllers.subscribe_controller import SubscribeController
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client, make_contract_wallet
from web3cli.helpers.render import render
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers.resolve import resolve_address
from web3core.helpers.rpc import check_ws_or_raise
from web3core.seeds.contracts.era_contract_seeds import nusdc


class EralendWatchController(SubscribeController):
    """Handler of the `w3 eralend-watch` commands"""

    class Meta:
        label = "eralend-watch"
        help = "Try to redeem USDC from the Eralend nUSDC pool as soon as some debt is paid"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Catch repay events and redeem",
        arguments=[
            (
                ["--contracts"],
                {
                    "help": "Consider only events emitted by these smart contracts",
                    "nargs": "+",
                    "default": [nusdc["address"]],
                },
            ),
            (
                ["--topics"],
                {
                    "help": "Consider only events with these topics",
                    "nargs": "+",
                    "default": [
                        "0x1a2a22cb034d26d1854bdc6666a5b91fe25efbbb5dcad3b0355478d6f5c362a1"
                    ],
                },
            ),
            (
                ["--redeem"],
                {
                    "help": "Attempt to redeem every time a repay event is detected",
                    "action": "store_true",
                },
            ),
            (
                ["--min-amount"],
                {
                    "help": "Minimum amount of USDC (in wei) worth redeeming",
                    "type": int,
                    "default": 5_000_000,
                },
            ),
            (
                ["--max-amount"],
                {
                    "help": "Maximum amount of USDC (in wei) to redeem in one go",
                    "type": int,
                    "default": 700_000_000,
                },
            ),
            (
                ["--reduce-by"],
                {
                    "help": "Reduce amount to redeem by this percentage",
                    "type": int,
                    "default": 10,
                },
            ),
            args.subscribe_print(),
            args.subscribe_senders(),
            *args.tg_args(),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            *args.tx_args(),
        ],
        aliases=["logs"],
    )
    def watch_repay(self) -> None:
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
                tx_on_fetch=lambda tx, data: self.app.log.debug(
                    f"Fetched tx {tx['hash'].hex()} from {tx['from']}"
                ),
                tx_on_fetch_error=lambda e, data: self.app.log.warning(e),
                on_connection_closed=lambda _, __: self.app.log.warning(
                    "Connection closed, reconnecting..."
                ),
            )
        )

    @ex(
        help="Repay USDC debt; use it with --dry-run flag to get the tx hash without sending it",
        arguments=[
            (["amount"], {"help": "Amount of USDC to repay", "type": int}),
            *args.signer_and_gas(),
            *args.tx_args(),
            *args.chain_and_rpc(),
        ],
    )
    def repay(self) -> None:
        signer = make_contract_wallet(self.app, "nusdc")
        output = send_contract_tx(
            self.app,
            signer,
            signer.functions["repayBorrow"](self.app.pargs.amount),
        )
        render(output)

    def get_callback(self) -> AsyncSubscriptionCallback:
        """Return the callback to invoke when a notification is received,
        based on the command arguments."""

        async def callback(data: Any, sub_type: SubscriptionType, tx: TxData) -> None:
            # PRINT CALLBACK
            if self.app.pargs.print:
                render(self.app, data)
            # REDEEM CALLBACK
            if self.app.pargs.redeem:
                signer = make_contract_wallet(self.app, "nusdc")
                # Get how much USDC was repaid
                repaid_amount = int(data["data"][2:][64:][64:][:64], 16)
                print(f"Somebody deposited {repaid_amount/10**6} USDC")
                # Compute how much to redeem
                redeem_amount = repaid_amount
                if self.app.pargs.reduce_by > 0:
                    redeem_amount = int(
                        redeem_amount * (1 - self.app.pargs.reduce_by / 100)
                    )
                if self.app.pargs.max_amount > 0:
                    redeem_amount = min(redeem_amount, self.app.pargs.max_amount)
                if redeem_amount < self.app.pargs.min_amount:
                    print("Skipping: too little USDC to redeem")
                    return
                try:
                    print(f"Attempting to redeem {redeem_amount/10**6} USDC...")
                    output = send_contract_tx(
                        self.app,
                        signer,
                        signer.functions["redeemUnderlying"](repaid_amount),
                    )
                except web3_exceptions.ContractCustomError as e:
                    print(f"😢 Too late: {e}")
                    return
                print("🎉 Might have succeeded:")
                print(output)

        return callback
