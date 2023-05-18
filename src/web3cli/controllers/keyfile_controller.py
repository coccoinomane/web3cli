import getpass
import json

from cement import ex
from eth_account import Account

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError


class KeyfileController(Controller):
    """Handler of the `w3 keyfile` commands"""

    class Meta:
        label = "keyfile"
        help = "create and read JSON keyfiles, like the ones used by geth, brownie, ape, etc"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Print the private key of the given keyfile",
        arguments=[
            (["path"], {"help": "path to input keyfile (JSON)"}),
        ],
        aliases=["decrypt"],
    )
    def decode(self) -> None:
        with open(self.app.pargs.path) as f:
            keyfile_json = json.load(f)
        password = getpass.getpass("Enter password to decrypt keyfile: ")
        try:
            private_key = Account.decrypt(keyfile_json, password)
        except ValueError as e:
            raise Web3CliError(f"Could not decrypt keyfile: {e}")
        self.app.print(str(private_key.hex()[2:]))

    @ex(
        help="Create a new keyfile from a private key",
        label="import",
        arguments=[
            (["path"], {"help": "path of output keyfile"}),
        ],
        aliases=["encrypt"],
    )
    def import_(self) -> None:
        private_key = getpass.getpass("Enter the private key, without the leading 0x: ")
        password = getpass.getpass("Enter a password to encrypt the keyfile: ")
        keyfile_json = Account.encrypt(private_key=private_key, password=password)
        json.dump(keyfile_json, open(self.app.pargs.path, "w"))
        self.app.log.info(f"Keyfile saved to {self.app.pargs.path}")
