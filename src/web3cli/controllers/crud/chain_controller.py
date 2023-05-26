from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.render import render_json, render_table
from web3core.exceptions import ChainNotFound
from web3core.models.chain import Chain
from web3core.seeds import chain_seeds


class ChainController(Controller):
    """Handler of the `w3 chain` CRUD commands"""

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
                ["--rpcs"],
                {
                    "help": "one or more RPCs for the chain",
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
            (["-d", "--desc"], {"action": "store"}),
        ],
    )
    def add(self) -> None:
        chain = Chain.get_by_name(self.app.pargs.name)
        if not chain or self.app.pargs.update:
            chain = Chain.upsert(
                {
                    "name": self.app.pargs.name,
                    "desc": self.app.pargs.desc,
                    "chain_id": self.app.pargs.chain_id,
                    "coin": self.app.pargs.coin,
                    "tx_type": self.app.pargs.tx_type,
                    "middlewares": None
                    if self.app.pargs.poa
                    else "geth_poa_middleware",
                },
                logger=self.app.log.info,
            )
        else:
            raise Web3CliError(
                f"Chain '{self.app.pargs.name}' already exists. Use `--update` or `-u` to update it."
            )

        # Create or update RPCs
        for rpc_url in self.app.pargs.rpcs:
            chain.add_rpc(rpc_url, self.app.log.info)

    @ex(help="list available chains")
    def list(self) -> None:
        render_table(
            self.app,
            headers=["NAME", "CHAIN ID", "COIN", "TX TYPE", "RPCS"],
            data=[
                [c.name, c.chain_id, c.coin, c.tx_type, len(c.get_rpcs())]
                for c in Chain.get_all(Chain.name)
            ],
        )

    @ex(
        help="show the details of the given chain",
        arguments=[(["name"], {"help": "the name of the chain to look up"})],
    )
    def get(self) -> None:
        render_json(self.app, Chain.get_as_dict(Chain.name == self.app.pargs.name))

    @ex(help="get the active chain's name", arguments=[args.chain()])
    def active(self) -> None:
        self.app.print(self.app.chain.name)

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
        chains = Chain.seed(chain_seeds.all, self.app.log.info)
        self.app.log.info(
            f"Imported {len(chains)} chains, run `w3 chain list` to show them"
        )
