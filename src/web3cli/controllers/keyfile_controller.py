import json

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers.crypto import decrypt_keyfile, encrypt_to_keyfile


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
        key = decrypt_keyfile(self.app.pargs.path)
        self.app.print(key.replace("0x", ""))

    @ex(
        help="Create a new keyfile from a private key",
        label="import",
        arguments=[
            (["path"], {"help": "path of output keyfile"}),
        ],
        aliases=["encode", "encrypt"],
    )
    def import_(self) -> None:
        keyfile_json = encrypt_to_keyfile()
        json.dump(keyfile_json, open(self.app.pargs.path, "w"))
        self.app.log.info(f"Keyfile saved to {self.app.pargs.path}")
