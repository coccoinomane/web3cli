from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.exceptions import ChainNotFound
from web3cli.core.models.chain import Chain, Rpc, ChainRpc
from web3cli.core.helpers.format import cut
import argparse


class RpcController(Controller):
    """Handler of the `web3 rpc` commands"""

    class Meta:
        label = "rpc"
        help = "add, list or delete rpcs"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="add a new rpc to the given chain",
        arguments=[
            (["chain_name"], {"help": "name of the chain of the rpc"}),
            (
                ["rpc"],
                {
                    "help": "url of the RPC to add; you can add more than one",
                    "nargs": "+",
                },
            ),
        ],
    )
    def add(self) -> None:
        chain = Chain.get_by_name(self.app.pargs.chain_name)
        if not chain:
            raise ChainNotFound(
                f"Chain '{self.app.pargs.chain_name}' does not exist, add it with `web3 chain add`"
            )

        for rpc_url in self.app.pargs.rpc:
            chain.add_rpc(rpc_url, self.app.log.info)

    @ex(
        help="list available rpcs and their chains",
    )
    def list(self) -> None:
        self.app.render(
            [
                [r.id, cut(r.url, 50), ",".join([c.name for c in r.get_chains()])]
                for r in Rpc.get_all()
            ],
            headers=["ID", "RPC", "CHAIN"],
            handler="tabulate",
        )

    @ex(
        help="show the full URL of the RPC with the given ID",
        arguments=[
            (
                ["id"],
                {
                    "help": "ID of the rpc; run `web3 rpc list` to list the IDs",
                    "type": int,
                },
            ),
        ],
    )
    def get_url(self) -> None:
        rpc = Rpc.get(self.app.pargs.id)
        self.app.print(rpc.url)

    @ex(
        help="delete one or more rpcs",
        arguments=[
            (
                ["ids"],
                {
                    "help": "IDs of the rpc to delete; run `web3 rpc list` to list the IDs",
                    "nargs": "+",
                    "type": int,
                },
            ),
        ],
    )
    def delete(self) -> None:
        for id in self.app.pargs.ids:
            rpc = Rpc.get(id)
            rpc.delete_instance()
            self.app.log.info(f"Rpc {id} deleted correctly [url => {rpc.url}]")
