from pprint import pformat
from cement import ex
from web3 import Web3
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.input import yes_or_exit
from web3cli.core.models.address import Address
from web3cli.helpers.version import get_version_message
from web3cli.helpers.client_factory import make_client, make_wallet
from web3cli.helpers import args
from web3cli import resolve_address


class Base(Controller):
    """Base controller. It:
    1. Defines top-level commands, such as `web3 balance`.
    2. Handles global arguments, such as --network
    3. Controls what happens when web3cli is invoked without arguments."""

    class Meta:
        label = "base"

        description = (
            "Interact with Ethereum and other blockchains with the command line"
        )

        # Arguments set in the base controller will be global and
        # recognized by all subcommands, as long as they are given
        # right after the web3cli command
        arguments = [
            (
                ["-v", "--version"],
                {"action": "version", "version": get_version_message()},
            ),
            (
                ["-n", "--network"],
                {
                    "action": "store",
                    "help": "network (blockchain) to use",
                },
            ),
            (
                ["-s", "--signer"],
                {
                    "action": "store",
                    "help": "wallet that will sign transactions (e.g. send tokens, interact with contracts, etc)",
                },
            ),
            (
                ["--priority-fee"],
                {
                    "action": "store",
                    "help": "max priority fee (tip) in gwei you are willing to spend for a transaction",
                    "type": int,
                    "default": 1,
                },
            ),
        ]

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(help="Show the version of web3")
    def version(self) -> None:
        self.app.print(get_version_message())

    @ex(
        help="Get the balance of the given address in the blockchain coin (ETH, BNB, AVAX, etc)",
        arguments=[(["address"], {"action": "store"})],
    )
    def balance(self) -> None:
        balance = make_client(self.app).getBalanceInEth(
            resolve_address(self.app.pargs.address)
        )
        self.app.render({"amount": balance, "ticker": self.app.coin}, "balance.jinja2")

    @ex(
        help="Transfer funds to the given address, denominated in the blockchain native coin (ETH, BNB, AVAX, etc)",
        arguments=[
            (
                ["to"],
                {
                    "help": "receiver of the funds; can be an actual address or an address tag",
                    "action": "store",
                },
            ),
            (["amount"], {"help": "how much to send", "action": "store"}),
            (
                ["unit"],
                {
                    "help": "optionally specify the unit to use (wei, gwei, etc)",
                    "default": "ether",
                    "action": "store",
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
        address = Address.resolve_address(self.app.pargs.to)
        if not self.app.pargs.force:
            ticker = (
                self.app.coin if self.app.pargs.unit == "ether" else self.app.pargs.unit
            )
            print(
                f"You are about to send {self.app.pargs.amount} {ticker} on the {self.app.network} chain from {self.app.signer} to {address}."
            )
            yes_or_exit(logger=self.app.log.info)
        tx_hash = make_wallet(self.app).sendEthInWei(
            to=address,
            valueInWei=Web3.toWei(self.app.pargs.amount, self.app.pargs.unit),
            maxPriorityFeePerGasInGwei=self.app.priority_fee,
        )
        self.app.print(tx_hash)

    @ex(
        help="Sign the given message and show the signed message, as returned by web3.py",
        arguments=[(["msg"], {"action": "store"})],
    )
    def sign(self) -> None:
        signed_message = make_wallet(self.app).signMessage(self.app.pargs.msg)
        self.app.print(pformat(signed_message._asdict()))

    def _post_argument_parsing(self) -> None:
        """Parse global arguments"""

        # Do nothing if no command is invoked (for example
        # if one simply runs `web3` or `web3 network`)
        if not args.get_command(self.app):
            return

        args.parse_global_args(self.app)
