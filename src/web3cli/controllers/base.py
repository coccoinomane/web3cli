from web3cli.core.controllers import Web3CliController
from web3cli.core.version import get_version_message
import web3cli.core.args as args


class Base(Web3CliController):
    """Controller for when web3cli is invoked with no arguments"""

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

    def _post_argument_parsing(self) -> None:
        """Handle global arguments"""

        # Command invoked from the CLI
        command: str = args.get_command(self.app)
        # Handle --network argument
        if command and command.startswith("network"):
            self.app.pargs.network = args.get_network(self.app)
            args.validate_network(self.app.pargs.network)
