from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.helpers.config import update_setting_in_config_file
import secrets
import sys


class KeyController(Controller):
    """Handler of the `w3 key` commands"""

    class Meta:
        label = "key"
        help = "handle passwords and application keys"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="generate a new random password and set it as the app key",
        arguments=[
            (
                ["-f", "--force"],
                {
                    "help": "if an app key already exists, replace it without asking (all signers added with the old app key will need to be recreated)",
                    "action": "store_true",
                },
            )
        ],
    )
    def create(self) -> None:
        # If the app key already exists, warn the user before replacing it
        key_exists = True if self.get_option("web3cli.app_key") else False
        if key_exists and not self.app.pargs.force:
            self.app.log.error(
                "App key already exists, run `w3 key create --force` to replace it.\nIf you do so, signers added with the old key will need to be recreated."
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
        self.app.print(str(key))
