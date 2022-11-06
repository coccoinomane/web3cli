from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.user import User as Model
from web3cli.core.exceptions import KeyIsInvalid
from eth_account import Account
import getpass


class User(Controller):
    class Meta:
        label = "user"
        help = "add, list or delete users"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list users")
    def list(self) -> None:
        self.app.render(
            [[u["label"], u["address"]] for u in Model.get_all(Model.label)],
            headers=["LABEL", "ADDRESS"],
            handler="tabulate",
        )

    # @ex(
    #     help="show a by its label",
    #     arguments=[
    #         (["label"], {"help": "label of the user to show", "action": "store"}),
    #     ],
    # )
    # def get(self) -> None:
    #     self.app.print(Model.get_address(self.app.pargs.label))

    @ex(
        help="add a new user",
        arguments=[
            (["label"], {"help": "label identifying the user", "action": "store"}),
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
        self.app.log.info(f"User '{self.app.pargs.label}' added correctly")

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

    @ex(help="get current user")
    def get(self) -> None:
        self.app.print(self.app.user)
