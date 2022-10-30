from cement import Controller, ex
from web3cli.src.helpers.networks import get_supported_networks, is_network_supported


class Network(Controller):
    class Meta:
        label = "network"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list available networks")
    def list(self):
        self.app.render({"networks": get_supported_networks()}, "network/list.jinja2")

    @ex(help="get current network")
    def get(self):
        print(self.app.config.get("web3cli", "network"))

    @ex(
        help="use the given network",
        arguments=[
            (["network"], {"action": "store", "help": "network to use"}),
        ],
    )
    def set(self):
        """TODO: This won't work unless we remove the network
        from the yaml, and put it in some form of DB"""
        network = self.app.pargs.network
        if not is_network_supported(network):
            raise Exception(f"Network {network} not supported")
        self.app.config.set("web3cli", "network", network)
