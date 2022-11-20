from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.address import Address
from web3cli.core.exceptions import Web3CliError, AddressIsInvalid


class AddressController(Controller):
    """Handler of the `web3 address` commands"""

    class Meta:
        label = "address"
        help = "add, list or delete addresses"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list address")
    def list(self) -> None:
        self.app.render(
            [
                [a["label"], a["address"]]
                for a in Address.get_all_as_dicts(Address.label)
            ],
            headers=["LABEL", "ADDRESS"],
            handler="tabulate",
        )

    @ex(
        help="show an address by its label",
        arguments=[
            (["label"], {"help": "label of the address to show"}),
        ],
    )
    def get(self) -> None:
        self.app.print(Address.get_address(self.app.pargs.label))

    @ex(
        help="add a new address",
        arguments=[
            (["label"], {"help": "label identifying the address"}),
            (["address"], {"help": "blockchain address (0x...)"}),
            (["-d", "--description"], {"action": "store"}),
            (
                ["-u", "--update"],
                {
                    "help": "if an address with the same label is present, overwrite it",
                    "action": "store_true",
                },
            ),
        ],
    )
    def add(self) -> None:
        if not Address.is_valid_address(self.app.pargs.address):
            raise AddressIsInvalid(f"Invalid address given: {self.app.pargs.address}")
        address = Address.get_by_label(self.app.pargs.label)
        if not address:
            Address.create(
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
            (["label"], {"help": "label of the address to delete"}),
        ],
    )
    def delete(self) -> None:
        address = Address.get_by_label_or_raise(self.app.pargs.label)
        address.delete_instance()
        self.app.log.info(f"Address '{self.app.pargs.label}' deleted correctly")
