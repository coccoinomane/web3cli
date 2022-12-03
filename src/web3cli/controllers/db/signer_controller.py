from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.signer import Signer
from web3cli.core.exceptions import KeyIsInvalid, SignerNotFound, Web3CliError
from web3cli.helpers.crypto import encrypt_string_with_app_key
from eth_account import Account
import getpass

from web3cli.helpers.render import render_table


class SignerController(Controller):
    """Handler of the `w3 db signer` commands"""

    class Meta:
        label = "signer"
        help = "add, list or delete signers"
        stacked_type = "nested"
        stacked_on = "db"

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
        help="show the address of a signer by its name; without arguments, show the name of the active signer",
        arguments=[
            (
                ["name"],
                {
                    "help": "name of the signer to show",
                    "nargs": "?",
                },
            ),
        ],
    )
    def get(self) -> None:
        if self.app.pargs.name:
            self.app.print(Signer.get_address(self.app.pargs.name))
        elif self.app.signer:
            self.app.print(self.app.signer)
        else:
            raise SignerNotFound(
                "Signer not set. Add one with `w3 db signer add <name>`"
            )

    @ex(
        help="add a new signer; you will be asked for the private key",
        arguments=[
            (["name"], {"help": "name identifying the signer"}),
            (
                ["--create"],
                {
                    "help": "generate a new private key instead, and use it to create the signer",
                    "action": "store_true",
                },
            ),
            (
                ["-p", "--private-key"],
                {
                    "help": "optionally, provide the private key directly; if you do so, make sure you clean your command history afterwards",
                },
            ),
        ],
    )
    def add(self) -> None:
        # Validate name
        if Signer.get_by_name(self.app.pargs.name):
            raise Web3CliError(
                f"Signer with name '{self.app.pargs.name}' already exists; to delete it, use `w3 db signer delete {self.app.pargs.name}`"
            )
        # Validate optional args
        if self.app.pargs.create and self.app.pargs.private_key:
            raise Web3CliError(
                "Arguments --create and --private-key are mutually exclusive"
            )
        # Case 1: private key passed via argument
        if self.app.pargs.private_key:
            key = self.app.pargs.private_key
        # Case 2: generate private key from scratch
        elif self.app.pargs.create:
            key = Account.create(self.app.app_key).key.hex()
        # Case 3: let the user input the key (default)
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
