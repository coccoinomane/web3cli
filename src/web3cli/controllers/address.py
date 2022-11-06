from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.address import Address as Model
from web3cli.core.exceptions import Web3CliError, AddressNotFound, AddressIsInvalid


class Address(Controller):
    class Meta:
        label = "address"
        help = "add, list or delete addresses"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list address")
    def list(self) -> None:
        self.app.render(
            [[a["label"], a["address"]] for a in Model.get_all(Model.label)],
            headers=["LABEL", "ADDRESS"],
            handler="tabulate",
        )

    @ex(
        help="show an address by its label",
        arguments=[
            (["label"], {"help": "label of the address to show", "action": "store"}),
        ],
    )
    def get(self) -> None:
        self.app.print(Model.get_address(self.app.pargs.label))

    @ex(
        help="add a new address",
        arguments=[
            (["label"], {"help": "label identifying the address", "action": "store"}),
            (["address"], {"help": "blockchain address (0x...)", "action": "store"}),
            (["-d", "--description"], {"action": "store"}),
            (
                ["-u", "--update"],
                {
                    "help": "if an address with the same label is present, overwrite it",
                    "action": "store_const",
                    "const": True,
                },
            ),
        ],
    )
    def add(self) -> None:
        if not Model.is_valid_address(self.app.pargs.address):
            raise AddressIsInvalid(f"Invalid address given: {self.app.pargs.address}")
        address = Model.get_by_label(self.app.pargs.label)
        if not address:
            Model.create(
                label=self.app.pargs.label,
                address=self.app.pargs.address,
                description=self.app.pargs.description,
            )
            self.app.log.info(f"Address '{self.app.pargs.label}' added correctly")
        elif self.app.pargs.update:
            address.address = self.app.pargs.address
            address.description = self.app.pargs.description
            address.save()
            self.app.log.info(f"Address '{self.app.pargs.label}' updated correctly")
        else:
            raise Web3CliError(
                f"Address '{self.app.pargs.label}' already exists with value {address.address}. Use `--update` or `-u` to update the address."
            )

    @ex(
        help="delete an address",
        arguments=[
            (["label"], {"help": "label of the address to delete", "action": "store"}),
        ],
    )
    def delete(self) -> None:
        address = Model.get_by_label(self.app.pargs.label)
        if not address:
            raise AddressNotFound(
                f"Address '{self.app.pargs.label}' does not exist, can't delete it"
            )
        address.delete_instance()
        self.app.log.info(f"Address '{self.app.pargs.label}' deleted correctly")
