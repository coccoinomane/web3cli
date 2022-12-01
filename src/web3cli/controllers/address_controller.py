from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.address import Address
from web3cli.core.exceptions import Web3CliError
from web3cli.helpers.render import render_table


class AddressController(Controller):
    """Handler of the `w3 address` commands"""

    class Meta:
        label = "address"
        help = "add, list or delete addresses"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list address")
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [a["name"], a["address"]]
                for a in Address.get_all_as_dicts(Address.name)
            ],
            headers=["NAME", "ADDRESS"],
            wrap=42,
        )

    @ex(
        help="show an address by its name",
        arguments=[
            (["name"], {"help": "name of the address to show"}),
        ],
    )
    def get(self) -> None:
        self.app.print(Address.get_address(self.app.pargs.name))

    @ex(
        help="add a new address",
        arguments=[
            (["name"], {"help": "name of the address"}),
            (["address"], {"help": "blockchain address (0x...)"}),
            (["-d", "--description"], {"action": "store"}),
            (
                ["-u", "--update"],
                {
                    "help": "if an address with the same name is present, overwrite it",
                    "action": "store_true",
                },
            ),
        ],
    )
    def add(self) -> None:
        address = Address.get_by_name(self.app.pargs.name)
        if not address or self.app.pargs.update:
            Address.upsert(
                {
                    "name": self.app.pargs.name,
                    "address": self.app.pargs.address,
                    "description": self.app.pargs.description,
                },
                logger=self.app.log.info,
            )
        else:
            raise Web3CliError(
                f"Address '{self.app.pargs.name}' already exists with value {address.address}. Use `--update` or `-u` to update the address."
            )

    @ex(
        help="delete an address",
        arguments=[
            (["name"], {"help": "name of the address to delete"}),
        ],
    )
    def delete(self) -> None:
        address = Address.get_by_name_or_raise(self.app.pargs.name)
        address.delete_instance()
        self.app.log.info(f"Address '{self.app.pargs.name}' deleted correctly")
