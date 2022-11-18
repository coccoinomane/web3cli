from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.networks import get_supported_networks


class ChainController(Controller):
    """Handler of the `web3 chain` commands"""

    class Meta:
        label = "chain"
        help = "show the chains available in web3cli"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list available chains")
    def list(self) -> None:
        self.app.render(
            [[n["name"], n["chainId"], n["coin"]] for n in get_supported_networks()],
            headers=["NAME", "CHAIN ID", "COIN"],
            handler="tabulate",
        )

    @ex(help="get current chain")
    def get(self) -> None:
        self.app.print(self.app.chain)
