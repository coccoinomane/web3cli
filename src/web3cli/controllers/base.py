from cement.utils.version import get_version_banner
from web3cli.core.controller import Web3CliController
from ..core.version import get_version

VERSION_BANNER = """
web3cli %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Base(Web3CliController):
    """Controller for when web3cli is invoked with no arguments"""

    class Meta:
        label = "base"

        description = (
            "Interact with Ethereum and other blockchains with the command line"
        )

        arguments = [
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()
