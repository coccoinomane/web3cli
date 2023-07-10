import secrets
import sys

from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.config import update_setting_in_config_file
from web3cli.helpers.render import render


class AppKeyController(Controller):
    """Handler of the `w3 app-key` commands"""

    class Meta:
        label = "app-key"
        help = "create the application key"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="generate a new random password and set it as the app key",
        arguments=[
            args.force(
                help="replace the key if it already exists; all signers will need to be recreated"
            ),
        ],
    )
    def create(self) -> None:
        # If the app key already exists, warn the user before replacing it
        key_exists = True if self.app.get_option("app_key") else False
        if key_exists and not self.app.pargs.force:
            self.app.log.error(
                "App key already exists, run `w3 app-key create --force` to replace it.\nIf you do so, signers added with the old key will need to be recreated."
            )
            self.app.exit_code = 0
            sys.exit()

        # Generate new app key and store it
        key = secrets.token_bytes(32)
        update_setting_in_config_file(
            self.app,
            setting="app_key",
            value=str(key),
            do_log=False,
            is_global=True,
        )
        self.app.log.info("Created app key")
        # Warn about old signers being useless now
        if key_exists:
            self.app.log.warning(
                "The old key was deleted: make sure to replace signers added with it"
            )

    @ex(
        help="generate and show a new random password, suitable to encrypt a private key; the password will not be stored anywhere, so take note of it if you want to use it!",
    )
    def generate(self) -> None:
        key = secrets.token_bytes(32)
        render(self.app, str(key))
