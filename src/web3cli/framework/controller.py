from cement import Controller as CementController

from web3cli.framework.app import App


class Controller(CementController):
    """Extend this class to define new commands"""

    def _default(self) -> None:
        """Default action if no sub-command is passed."""
        self.app.args.print_help()

    def __init__(self) -> None:
        """Make self.app attributes discoverable by IDEs. See
        https://github.com/datafolklabs/cement/issues/599
        for more details"""
        super().__init__()
        self.app: App
