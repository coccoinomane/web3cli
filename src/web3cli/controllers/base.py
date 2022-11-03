from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.helpers.version import get_version_message
from web3cli.helpers.factory import make_client
from web3cli.core.helpers.networks import get_coin
from web3cli.helpers import args


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
        ]

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    @ex(
        help="Get the balance of the given address in the blockchain coin (ETH, BNB, AVAX, etc)",
        arguments=[(["address"], {"action": "store"})],
    )
    def balance(self) -> None:
        balance = make_client(self.app).getBalanceInEth(self.app.pargs.address)
        self.app.render({"amount": balance, "ticker": self.app.coin}, "balance.jinja2")

    def _post_argument_parsing(self) -> None:
        """Parse and handle global arguments"""

        # Do nothing if no command is invoked (for example
        # if one simply runs `web3` or `web3 network`)
        if not args.get_command(self.app):
            return

        # Save the network provided by the user
        self.app.extend("network", args.parse_network(self.app))  # ethereum binance etc
        self.app.extend("coin", get_coin(self.app.network))  # ETH BNB etc
