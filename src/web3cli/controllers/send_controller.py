from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.input import yes_or_exit
from web3cli.core.models.address import Address
from web3cli.helpers.send import send_coin_or_token


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
            (["amount"], {"help": "how much to send", "type": float}),
            (
                ["ticker"],
                {"help": "ticker of the coin or token to send"},
            ),
            (
                ["unit"],
                {
                    "help": "optionally specify the unit to use (wei, gwei, etc)",
                    "nargs": "?",
                    "default": "ether",
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
        # Parse arguments
        to_address = Address.resolve_address(self.app.pargs.to)
        if not self.app.pargs.force:
            what = f"{self.app.pargs.amount} {self.app.pargs.ticker}"
            if self.app.pargs.unit != "ether":
                what = f"{self.app.pargs.amount} {self.app.pargs.unit} units of {self.app.pargs.ticker}"
            print(
                f"You are about to send {what} on the {self.app.chain} chain from signer {self.app.signer} to {to_address}."
            )
            yes_or_exit(logger=self.app.log.info)
        # Send
        tx_hash = send_coin_or_token(
            self.app,
            ticker=self.app.pargs.ticker,
            to=to_address,
            amount=self.app.pargs.amount,
            unit=self.app.pargs.unit,
        )
        self.app.print(tx_hash)
