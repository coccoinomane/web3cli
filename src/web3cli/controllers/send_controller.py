from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render
from web3cli.helpers.send import send_coin_or_token
from web3core.helpers.misc import to_number, yes_or_exit
from web3core.helpers.resolve import resolve_address


class SendController(Controller):
    """Handler of the `w3 send` command"""

    class Meta:
        label = "send"
        help = "send native coins, tokens and NFTs"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Send a coin or token to the given address, and show the transaction hash",
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
                    "help": "optionally specify the unit to use. For native-coins: wei, gwei, etc. For tokens: specify 'smallest' to send using the smallest unit of the token.",
                    "nargs": "?",
                },
            ),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            args.force(),
        ],
    )
    def send(self) -> None:
        # Parse arguments
        to_address = resolve_address(self.app.pargs.to, chain=self.app.chain.name)
        amount = to_number(self.app.pargs.amount)
        ticker = self.app.pargs.ticker.lower()
        if not self.app.pargs.force:
            what = f"{amount} {ticker}"
            if self.app.pargs.unit:
                what = f"{amount} {self.app.pargs.unit} unit(s) of {ticker}"
            print(
                f"You are about to send {what} on the {self.app.chain.name} chain from {self.app.signer.address} to {to_address}."
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
        render(self.app, tx_hash)
