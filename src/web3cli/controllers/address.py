from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.address import Address as Model


class Address(Controller):
    class Meta:
        label = "address"
        help = "add, list or delete addresses"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list address")
    def list(self) -> None:
        addresses = [a for a in Model.select().order_by(Model.label).dicts()]
        self.app.render({"addresses": addresses}, "address/list.jinja2")

    @ex(
        help="add a new address",
        arguments=[
            (["address"], {"help": "blockchain address (0x...)", "action": "store"}),
            (["label"], {"help": "label identifying the address", "action": "store"}),
            (["-d", "--description"], {"action": "store"}),
        ],
    )
    def add(self) -> None:
        Model.create(
            address=self.app.pargs.address,
            label=self.app.pargs.label,
            description=self.app.pargs.description,
        )

    @ex(
        help="delete an address",
        arguments=[
            (["label"], {"help": "label of the address to delete", "action": "store"}),
        ],
    )
    def delete(self) -> None:
        Model.get_by_label(self.app.pargs.label).delete()
