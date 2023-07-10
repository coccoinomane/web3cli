import json

from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers.crypto import decrypt_keyfile, encrypt_to_keyfile
from web3cli.helpers.render import render


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
        render(self.app, key.replace("0x", ""))

    @ex(
        help="Create a new keyfile from a private key",
        arguments=[
            (
                ["path"],
                {
                    "help": "path of output keyfile; omit to print to screen",
                    "nargs": "?",
                },
            ),
        ],
        aliases=["encode", "encrypt"],
    )
    def create(self) -> None:
        keyfile_dict = encrypt_to_keyfile()
        if self.app.pargs.path:
            json.dump(keyfile_dict, open(self.app.pargs.path, "w"))
            self.app.log.info(f"Keyfile saved to {self.app.pargs.path}")
        else:
            render(self.app, json.dumps(keyfile_dict))
