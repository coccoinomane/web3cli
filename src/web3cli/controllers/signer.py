from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.signer import Signer as Model
from web3cli.core.exceptions import KeyIsInvalid
from eth_account import Account
import getpass


class Signer(Controller):
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

    # @ex(
    #     help="show a by its label",
    #     arguments=[
    #         (["label"], {"help": "label of the signer to show", "action": "store"}),
    #     ],
    # )
    # def get(self) -> None:
    #     self.app.print(Model.get_address(self.app.pargs.label))

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
            key=key,
            address=address,
        )
        self.app.log.info(f"Signer '{self.app.pargs.label}' added correctly")

    # @ex(
    #     help="delete an address",
    #     arguments=[
    #         (["label"], {"help": "label of the address to delete", "action": "store"}),
    #     ],
    # )
    # def delete(self) -> None:
    #     address = Model.get_by_label(self.app.pargs.label)
    #     if not address:
    #         raise AddressNotFound(
    #             f"Address '{self.app.pargs.label}' does not exist, can't delete it"
    #         )
    #     address.delete_instance()
    #     self.app.log.info(f"Address '{self.app.pargs.label}' deleted correctly")

    @ex(help="get current signer")
    def get(self) -> None:
        self.app.print(self.app.signer)
