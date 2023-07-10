from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render
from web3cli.helpers.version import get_version_message


class BaseController(Controller):
    """Base controller. Can be used to implement global arguments"""

    class Meta:
        label = "base"

        description = (
            "Interact with Ethereum and other blockchains with the command line"
        )

        # Arguments set in the base controller will be global and
        # recognized by all subcommands, as long as they are given
        # right after `w3`
        arguments = [
            (
                ["-v", "--version"],
                {"action": "version", "version": get_version_message()},
            )
        ]

    @ex(help="Show the app version")
    def version(self) -> None:
        render(self.app, get_version_message())

    def _post_argument_parsing(self) -> None:
        """Parse global arguments"""

        # Do nothing if no command is invoked (for example
        # if one simply runs `w3` or `w3 db`)
        if not args.get_command(self.app):
            return

        args.pre_parse_args(self.app)
