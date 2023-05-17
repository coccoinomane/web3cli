import getpass

from cement import ex
from eth_keyfile import decode_keyfile_json, load_keyfile

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
            (["keyfile"], {"help": "path to the JSON"}),
        ],
    )
    def decode(self) -> None:
        keyfile_json = load_keyfile(self.app.pargs.keyfile)
        password = getpass.getpass("Enter password to decrypt keyfile: ")
        try:
            private_key = decode_keyfile_json(keyfile_json, password)
        except ValueError as e:
            raise Web3CliError(f"Could not decrypt keyfile: {e}")
        self.app.print(str(private_key.hex()[2:]))
