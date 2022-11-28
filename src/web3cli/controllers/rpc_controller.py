from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.exceptions import ChainNotFound, Web3CliError
from web3cli.core.models.chain import Chain, Rpc, ChainRpc

from web3cli.helpers.render import render_table


class RpcController(Controller):
    """Handler of the `w3 rpc` commands"""

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
                ["rpcs"],
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
                f"Chain '{self.app.pargs.chain_name}' does not exist, add it with `w3 chain add`"
            )

        for rpc_url in self.app.pargs.rpcs:
            chain.add_rpc(rpc_url, self.app.log.info)

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
        self.app.print(rpc.url)

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
        ],
    )
    def get(self) -> None:
        # Case 1: Show the URL of the RPC with the given ID
        if self.app.pargs.id:
            rpc = Rpc.get_or_none(self.app.pargs.id)
            if not rpc:
                raise Web3CliError(f"RPC with ID {self.app.pargs.id} does not exist")
            self.app.print(rpc.url)
        # Case 2: RPC was forced via CLI argument
        elif self.app.rpc:
            self.app.print(self.app.rpc)
        # Case 3: show RPC inferred by the app
        else:
            chain = Chain.get_by_name_or_raise(self.app.chain)
            rpc = chain.pick_rpc()
            self.app.print(rpc.url)

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
