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
            ),
            (
                ["--network"],
                dict(help="which network to use", dest="network", action="store"),
            ),
        ]

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    def _post_argument_parsing(self) -> None:
        """Hooks called in every controller after argument
        parsing, before command execution"""

        # Set the passed network as the global variable network_name
        if self.app.pargs.network:
            self.app.extend("network_name", self.app.pargs.network)
        else:
            self.app.extend(
                "network_name", self.app.config.get("web3cli", "default_network")
            )
