from pprint import pformat
from cement import ex
from web3cli.controllers.controller import Controller
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
                    "dest": "network",
                    "help": "network (blockchain) to use",
                },
            ),
            (
                ["-s", "--signer"],
                {
                    "action": "store",
                    "dest": "signer",
                    "help": "wallet that will sign transactions (e.g. send tokens, interact with contracts, etc)",
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
