from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.helpers.version import get_version_message
from web3cli.helpers import args


class BaseController(Controller):
    """Base controller; it handles global arguments such as --chain
    and --signer"""

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
                ["-c", "--chain"],
                {
                    "help": "blockchain to use",
                },
            ),
            (
                ["-s", "--signer"],
                {
                    "help": "wallet that will sign transactions (e.g. send tokens, interact with contracts, etc)",
                },
            ),
            (
                ["--priority-fee"],
                {
                    "help": "max priority fee (tip) in gwei you are willing to spend for a transaction",
                    "type": int,
                    "default": 1,
                },
            ),
            (
                ["--rpc"],
                {
                    "help": "use this RPC url no matter what, ignoring whatever values were added previously"
                },
            ),
        ]

    @ex(help="Show the version of web3cli")
    def version(self) -> None:
        self.app.print(get_version_message())

    def _post_argument_parsing(self) -> None:
        """Parse global arguments"""

        # Do nothing if no command is invoked (for example
        # if one simply runs `w3` or `w3 db`)
        if not args.get_command(self.app):
            return

        args.parse_global_args(self.app)
