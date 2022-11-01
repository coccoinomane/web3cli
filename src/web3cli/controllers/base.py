from web3cli.core.controller import Web3CliController
from web3cli.core.version import get_version_message


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
            )
        ]

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    def _post_argument_parsing(self) -> None:
        """Hooks called in every controller after argument
        parsing, before command execution"""
        pass
