from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render, render_table
from web3core.models.chain import Rpc


class RpcController(Controller):
    """Handler of the `w3 rpc` CRUD commands"""

    class Meta:
        label = "rpc"
        help = "add, list or delete rpcs"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="add a new rpc to the given chain or to the active chain",
        arguments=[
            (
                ["rpcs"],
                {
                    "help": "url of the RPC to add; you can add more than one",
                    "nargs": "+",
                },
            ),
            args.chain(),
        ],
    )
    def add(self) -> None:
        for rpc_url in self.app.pargs.rpcs:
            self.app.chain.add_rpc(rpc_url, self.app.log.info)

    @ex(
        help="list available rpcs and their chains",
    )
    def list(self) -> None:
        render_table(
            self.app,
            headers=["ID", "RPC", "CHAIN"],
            data=[
                [r.id, r.url, ",".join([c.name for c in r.get_chains()])]
                for r in Rpc.get_all()
            ],
        )

    @ex(
        help="show the full URL of the RPC with the given ID",
        arguments=[
            (
                ["id"],
                {
                    "help": "ID of the rpc; run `w3 rpc list` to list the IDs",
                    "type": int,
                },
            ),
        ],
    )
    def get_url(self) -> None:
        rpc = Rpc.get(self.app.pargs.id)
        render(self.app, rpc.url)

    @ex(
        help="show the URL of an RPC by its ID; without arguments, shows the RPC that will be used by the CLI",
        arguments=[
            (
                ["id"],
                {
                    "help": "ID of the RPC to show; run `w3 rpc list` to list the IDs",
                    "nargs": "?",
                    "type": int,
                },
            ),
            *args.chain_and_rpc(),
        ],
    )
    def get(self) -> None:
        # Case 1: Show the URL of the RPC with the given ID
        if self.app.pargs.id:
            rpc = Rpc.get(self.app.pargs.id)
            render(self.app, rpc.url)
        # Case 2: RPC was forced via CLI argument
        else:
            render(self.app, self.app.rpc.url)

    @ex(
        help="delete one or more rpcs",
        arguments=[
            (
                ["ids"],
                {
                    "help": "IDs of the rpc to delete; run `w3 rpc list` to list the IDs",
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
