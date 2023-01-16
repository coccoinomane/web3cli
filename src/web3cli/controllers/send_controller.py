from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.send import send_coin_or_token
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.helpers.misc import to_number, yes_or_exit
from web3core.helpers.resolve import resolve_address
from web3core.models.address import Address
from web3core.models.signer import Signer


class SendController(Controller):
    """Handler of the `w3 send` command"""

    class Meta:
        label = "send"
        help = "send native coins, tokens and NFTs"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Send a coin or token to the given address and show the transaction hash",
        arguments=[
            (
                ["to"],
                {
                    "help": "receiver of the funds; can be an actual address or an address tag",
                },
            ),
            (["amount"], {"help": "how much to send"}),
            (
                ["ticker"],
                {"help": "ticker of the coin or token to send"},
            ),
            (
                ["unit"],
                {
                    "help": "optionally specify the unit to use (wei, gwei, etc)",
                    "nargs": "?",
                },
            ),
            (
                ["-f", "--force"],
                {
                    "help": "do not ask for confirmation",
                    "action": "store_true",
                },
            ),
        ],
    )
    def send(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        # Parse arguments
        to_address = resolve_address(self.app.pargs.to, [Address, Signer])
        amount = to_number(self.app.pargs.amount)
        ticker = self.app.pargs.ticker.lower()
        if not self.app.pargs.force:
            what = f"{amount} {ticker}"
            if self.app.pargs.unit:
                what = f"{amount} {self.app.pargs.unit} unit(s) of {ticker}"
            print(
                f"You are about to send {what} on the {self.app.chain.name} chain from signer {self.app.signer} to {to_address}."
            )
            yes_or_exit(logger=self.app.log.info)
        # Send
        tx_hash = send_coin_or_token(
            self.app,
            ticker=ticker,
            to=to_address,
            amount=amount,
            unit=self.app.pargs.unit,
        )
        self.app.print(tx_hash)
