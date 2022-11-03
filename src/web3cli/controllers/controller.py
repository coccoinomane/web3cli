from typing import Any
from cement import Controller as CementController
from cement.core.config import ConfigInterface
from cement import App


class Controller(CementController):
    """Extend this class to define new commands"""

    def __init__(self) -> None:
        """Make app attributes discoverable by IDEs. See
        https://github.com/datafolklabs/cement/issues/599
        for more details"""
        super().__init__()
        self.app = self.get_app()

    def get_app(self) -> App:
        """Get app object, with typing"""
        return self.app

    def get_config(self) -> ConfigInterface:
        """Get config object, with typing"""
        return self.app.config

    def get_option(self, option: str) -> Any:
        """Quickly access options Laravel style.
        Use the dot to separate section & option name.
        Example: get_option("section.option")"""
        parts = option.split(".", 1)
        return self.get_config().get(parts[0], parts[1])
