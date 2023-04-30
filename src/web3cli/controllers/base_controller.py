from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.version import get_version_message


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
            args.chain(),
            args.signer(),
            args.priority_fee(),
            args.rpc(),
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
