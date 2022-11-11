from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.signer import Signer as Model
from web3cli.core.exceptions import KeyIsInvalid, SignerNotFound, Web3CliError
from web3cli.helpers.crypto import encrypt_string_with_app_key
from eth_account import Account
import getpass


class Signer(Controller):
    """Handler of the `web3 signer` commands"""

    class Meta:
        label = "signer"
        help = "add, list or delete signers"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list signers")
    def list(self) -> None:
        self.app.render(
            [[u["label"], u["address"]] for u in Model.get_all(Model.label)],
            headers=["LABEL", "ADDRESS"],
            handler="tabulate",
        )

    @ex(
        help="show the address of a signer by its label; without arguments, show the label of the active signer",
        arguments=[
            (
                ["label"],
                {
                    "help": "label of the signer to show",
                    "nargs": "?",
                    "action": "store",
                },
            ),
        ],
    )
    def get(self) -> None:
        if self.app.pargs.label:
            self.app.print(Model.get_address(self.app.pargs.label))
        elif self.app.signer:
            self.app.print(self.app.signer)
        else:
            raise SignerNotFound(
                "Signer not set. Add one with `web3 signer add <label>`"
            )

    @ex(
        help="add a new signer; you will be asked for the private key",
        arguments=[
            (["label"], {"help": "label identifying the signer", "action": "store"}),
            (
                ["-p", "--private-key"],
                {
                    "help": "private key of the signer (NOT SAFE, use only at your risk)",
                    "action": "store",
                },
            ),
        ],
    )
    def add(self) -> None:
        # Validate label
        if Model.get_by_label(self.app.pargs.label):
            raise Web3CliError(
                f"Signer with label '{self.app.pargs.label}' already exists; to delete it, use `web3 signer delete {self.app.pargs.label}`"
            )
        # Parse and validate key
        key = self.app.pargs.private_key or getpass.getpass("Private key: ")
        try:
            address = Account.from_key(key).address
        except:
            raise KeyIsInvalid(
                "Invalid private key. Please note that private key is different from mnemonic password."
            )
        # Create signer
        Model.create(
            label=self.app.pargs.label,
            key=encrypt_string_with_app_key(self.app, key),
            address=address,
        )
        self.app.log.info(
            f"Signer '{self.app.pargs.label}' added correctly (address={address})"
        )

    @ex(
        help="delete a signer",
        arguments=[
            (["label"], {"help": "label of the signer to delete", "action": "store"}),
        ],
    )
    def delete(self) -> None:
        signer = Model.get_by_label(self.app.pargs.label)
        if not signer:
            raise SignerNotFound(
                f"Signer '{self.app.pargs.label}' does not exist, can't delete it"
            )
        signer.delete_instance()
        self.app.log.info(f"Signer '{self.app.pargs.label}' deleted correctly")
