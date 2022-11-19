from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.chain import Chain
from web3cli.core.seeds.chains import seed_chains


class ChainController(Controller):
    """Handler of the `web3 chain` commands"""

    class Meta:
        label = "chain"
        help = "add, list or delete chains"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list available chains")
    def list(self) -> None:
        self.app.render(
            [
                [c["name"], c["chain_id"], c["coin"], c["tx_type"]]
                for c in Chain.get_all(Chain.name)
            ],
            headers=["NAME", "CHAIN ID", "COIN", "TX TYPE"],
            handler="tabulate",
        )

    @ex(help="get current chain")
    def get(self) -> None:
        self.app.print(self.app.chain)

    @ex(help="preload a few chains")
    def seed(self) -> None:
        chains = Chain.seed(seed_chains)
        self.app.log.info(
            f"Imported {len(chains)} chains, run `web3 chain list` to show them"
        )
