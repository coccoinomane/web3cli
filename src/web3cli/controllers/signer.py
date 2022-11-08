from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.signer import Signer as Model
from web3cli.core.exceptions import KeyIsInvalid, SignerNotFound
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
        help="show the address of a signer by its label; without arguments, show the label of the signer that will be used by web3cli",
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
        else:
            self.app.print(self.app.signer)

    @ex(
        help="add a new signer",
        arguments=[
            (["label"], {"help": "label identifying the signer", "action": "store"}),
        ],
    )
    def add(self) -> None:
        key = getpass.getpass("Private key: ")
        try:
            address = Account.from_key(key).address
        except:
            raise KeyIsInvalid(
                "Invalid private key. Please note that private key is different from mnemonic password."
            )
        Model.create(
            label=self.app.pargs.label,
            key=encrypt_string_with_app_key(self.app, key),
            address=address,
        )
        self.app.log.info(f"Signer '{self.app.pargs.label}' added correctly")

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
