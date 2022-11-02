from cement import ex
from web3cli.core.controllers import Web3CliController
from web3cli.src.helpers.networks import get_supported_networks


class Network(Web3CliController):
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
