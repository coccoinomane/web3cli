from cement import ex

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers.render import render, render_table
from web3core.models.address import Address


class AddressController(Controller):
    """Handler of the `w3 address` CRUD commands"""

    class Meta:
        label = "address"
        help = "add, edit, list or delete addresses"
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
        help="show the details of the given address by name",
        arguments=[
            (["name"], {"help": "name of the address to show"}),
        ],
    )
    def get(self) -> None:
        render(self.app, Address.get_as_dict(Address.name == self.app.pargs.name))

    @ex(
        help="add a new address",
        arguments=[
            (["name"], {"help": "name of the address"}),
            (["address"], {"help": "blockchain address (0x...)"}),
            (["-d", "--desc"], {"action": "store"}),
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
                    "desc": self.app.pargs.desc,
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
