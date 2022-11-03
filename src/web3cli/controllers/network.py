from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.networks import get_supported_networks


class Network(Controller):
    """Controller for the `web3 network` commands"""

    class Meta:
        label = "network"
        help = "show the networks (blockchains) available in web3cli"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list available networks")
    def list(self) -> None:
        self.app.render({"networks": get_supported_networks()}, "network/list.jinja2")

    @ex(help="get current network")
    def get(self) -> None:
        print(self.app.pargs.network)
