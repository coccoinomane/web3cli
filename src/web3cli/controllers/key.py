from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.helpers.config import update_setting
import secrets
import sys


class Key(Controller):
    """Handler of the `web3 key` commands"""

    class Meta:
        label = "key"
        help = "handle password and application keys"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="generate a new random password and use it as the app key",
    )
    def create(self) -> None:
        # If the app key already exists, warn the user before replacing it
        if self.get_option("web3cli.app_key"):
            proceed = input(
                "An app key already exists, do you want to replace it?\nIf you do, you will need to recreate all signers that\nwere created without a custom password.\nType 'yes' to replace it: "
            )
            if proceed not in ("y", "yes"):
                self.app.log.info("Exiting...")
                self.app.exit_code = 0
                sys.exit()

        # Generate new app key and store it
        key = secrets.token_bytes(32)
        update_setting(
            self.app,
            setting="app_key",
            value=str(key),
            do_log=False,
            is_global=True,
        )
        self.app.log.info("Created new app key")

    @ex(
        help="generate a new random password, suitable to encrypt a private key; the password will not be stored anywhere, so take note of it if you use it!",
    )
    def generate(self) -> None:
        key = secrets.token_bytes(32)
        self.app.print(str(key))
