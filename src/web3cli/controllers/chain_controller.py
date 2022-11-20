from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.exceptions import ChainNotFound, Web3CliError
from web3cli.core.models.chain import Chain, ChainRpc, Rpc
from web3cli.core.models.types import ChainFields
from web3cli.core.seeds.chains import seed_chains


class ChainController(Controller):
    """Handler of the `web3 chain` commands"""

    class Meta:
        label = "chain"
        help = "add, list or delete chains"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="add a new chain",
        arguments=[
            (["name"], {"help": "unique name for the chain"}),
            (
                ["chain_id"],
                {"help": "Chain ID, e.g. 1 for Ethereum, 56 for Binance", "type": int},
            ),
            (["coin"], {"help": "ticker of the native coin of the chain"}),
            (
                ["--tx-type"],
                {
                    "help": "set to 1 if the chain does not implement EIP-1559 transactions (e.g. Binance and Avalanche); default is 2",
                    "default": 2,
                    "type": int,
                },
            ),
            (
                ["--poa"],
                {
                    "help": "set this flag if the chain needs a POA middleware (e.g. Binance, Avalanche, etc)",
                    "action": "store_true",
                },
            ),
            (
                ["--rpc"],
                {
                    "help": "URL of the chain RPC; you can add as many URLs as you wish",
                    "nargs": "+",
                    "default": [],
                },
            ),
            (
                ["-u", "--update"],
                {
                    "help": "if a chain with the same name is present, overwrite it",
                    "action": "store_true",
                },
            ),
        ],
    )
    def add(self) -> None:
        # Create or update chain
        fields: ChainFields = {
            "name": self.app.pargs.name,
            "chain_id": self.app.pargs.chain_id,
            "coin": self.app.pargs.coin.upper(),
            "tx_type": self.app.pargs.tx_type,
            "middlewares": None if self.app.pargs.poa else "geth_poa_middleware",
        }
        chain = Chain.get_by_name(self.app.pargs.name)
        if not chain:
            chain = Chain.create(**fields)
            self.app.log.info(f"Chain '{self.app.pargs.name}' added correctly")
        elif self.app.pargs.update:
            Chain.update(**fields).where(Chain.id == chain.id).execute()
            self.app.log.info(f"Chain '{self.app.pargs.name}' updated correctly")
        else:
            raise Web3CliError(
                f"Chain '{self.app.pargs.name}' already exists. Use `--update` or `-u` to update it."
            )

        # Create or update RPCs
        for rpc_url in self.app.pargs.rpc:
            chain.add_rpc(rpc_url, self.app.log.info)

    @ex(help="list available chains")
    def list(self) -> None:
        self.app.render(
            [
                [c["name"], c["chain_id"], c["coin"], c["tx_type"]]
                for c in Chain.get_all_as_dicts(Chain.name)
            ],
            headers=["NAME", "CHAIN ID", "COIN", "TX TYPE"],
            handler="tabulate",
        )

    @ex(help="get current chain")
    def get(self) -> None:
        self.app.print(self.app.chain)

    @ex(
        help="delete a chain",
        arguments=[
            (["name"], {"help": "name of the chain to delete"}),
        ],
    )
    def delete(self) -> None:
        chain = Chain.get_by_name(self.app.pargs.name)
        if not chain:
            raise ChainNotFound(
                f"Chain '{self.app.pargs.name}' does not exist, can't delete it"
            )
        chain.delete_instance()
        self.app.log.info(f"Chain '{self.app.pargs.name}' deleted correctly")

    @ex(help="preload a few chains")
    def seed(self) -> None:
        chains = Chain.seed(seed_chains, self.app.log.info)
        self.app.log.info(
            f"Imported {len(chains)} chains, run `web3 chain list` to show them"
        )
