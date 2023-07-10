import getpass

from cement import ex
from eth_account import Account

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.crypto import decrypt_keyfile, encrypt_string_with_app_key
from web3cli.helpers.render import render, render_table
from web3cli.helpers.signer import get_signer
from web3core.exceptions import KeyIsInvalid, SignerNotFound
from web3core.helpers.misc import are_mutually_exclusive
from web3core.models.signer import Signer


class SignerController(Controller):
    """Handler of the `w3 signer` CRUD commands"""

    class Meta:
        label = "signer"
        help = "add, list or delete signers"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list signers")
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [s["name"], s["address"]] for s in Signer.get_all_as_dicts(Signer.name)
            ],
            headers=["NAME", "ADDRESS"],
            wrap=42,
        )

    @ex(
        help="show the details of the given signer",
        arguments=[
            (
                ["name"],
                {
                    "help": "the signer to show; can be either a name, address, private key or keyfile"
                },
            )
        ],
    )
    def get(self) -> None:
        signer = get_signer(self.app, self.app.pargs.name).as_dict()
        signer["key"] = "********"
        render(self.app, signer)

    @ex(
        help="show the active signer's address",
        arguments=[
            (
                ["--show-name"],
                {
                    "help": "show the name of the active signer, instead",
                    "action": "store_true",
                },
            ),
            args.signer(),
        ],
    )
    def active(self) -> None:
        if self.app.pargs.show_name:
            render(self.app, self.app.signer.name)
        else:
            render(self.app, self.app.signer.address)

    @ex(
        help="add a new signer; you will be asked for the private key",
        arguments=[
            (["name"], {"help": "name identifying the signer"}),
            (
                ["--create"],
                {
                    "help": "generate a new private key instead, and use it to create the signer; then print the private key",
                    "action": "store_true",
                },
            ),
            (
                ["-p", "--private-key"],
                {
                    "help": "optionally, provide the private key directly; if you do so, make sure you clean your command history afterwards",
                },
            ),
            (
                ["--keyfile"],
                {
                    "help": "optionally, provide the path to a keyfile to import the private key from"
                },
            ),
        ],
    )
    def add(self) -> None:
        # Validate name
        if Signer.get_by_name(self.app.pargs.name):
            raise Web3CliError(
                f"Signer with name '{self.app.pargs.name}' already exists; to delete it, use `w3 signer delete {self.app.pargs.name}`"
            )
        # Validate optional args
        if not are_mutually_exclusive(
            self.app.pargs.create,
            bool(self.app.pargs.keyfile),
            bool(self.app.pargs.private_key),
        ):
            raise Web3CliError(
                "Arguments --create, --private-key and --keyfile cannot coexist"
            )
        # Case 1: private key passed via argument
        if self.app.pargs.private_key:
            key = self.app.pargs.private_key
        # Case 2: generate private key from scratch
        elif self.app.pargs.create:
            key = Account.create(self.app.app_key).key.hex()
        # Case 3: json keyfile passed via argument
        elif self.app.pargs.keyfile:
            key = decrypt_keyfile(self.app.pargs.keyfile)
        # Case 4: let the user input the key (default)
        else:
            key = getpass.getpass("Private key: ")
        # Verify key
        try:
            address = Account.from_key(key).address
        except:
            raise KeyIsInvalid(
                "Invalid private key. Please note that private key is different from mnemonic password."
            )
        # Create signer
        Signer.create(
            name=self.app.pargs.name,
            key=encrypt_string_with_app_key(self.app, key),
            address=address,
        )
        self.app.log.info(
            f"Signer '{self.app.pargs.name}' added correctly (address={address})"
        )
        if self.app.pargs.create:
            # Print private key
            render(self.app, key)

    @ex(
        help="delete a signer",
        arguments=[
            (["name"], {"help": "name of the signer to delete"}),
        ],
    )
    def delete(self) -> None:
        signer = Signer.get_by_name(self.app.pargs.name)
        if not signer:
            raise SignerNotFound(
                f"Signer '{self.app.pargs.name}' does not exist, can't delete it"
            )
        signer.delete_instance()
        self.app.log.info(f"Signer '{self.app.pargs.name}' deleted correctly")
