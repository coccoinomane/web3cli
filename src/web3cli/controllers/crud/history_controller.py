from cement import ex
from playhouse.shortcuts import model_to_dict

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render, render_table
from web3core.helpers.format import cut
from web3core.models.tx import Tx


class HistoryController(Controller):
    """Handler of the `w3 history` CRUD commands"""

    class Meta:
        label = "history"
        help = "add, list or delete transactions to the transaction history"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(help="list transactions in the history")
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [tx.hash, tx.chain, tx.created_at_short(), cut(tx.from_, 10)]
                for tx in Tx.get_all(Tx.created_at.desc())
            ],
            headers=["HASH", "CHAIN", "CREATED AT", "FROM"],
            wrap=66,
        )

    @ex(
        help="show details of the given transaction in the history",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
        ],
    )
    def get(self) -> None:
        tx = Tx.get_by_hash_or_raise(self.app.pargs.hash)
        render(self.app, model_to_dict(tx))

    @ex(
        help="add a new transaction to the history",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            (
                ["from"],
                {
                    "help": "address from which the tx was sent (0x...)",
                },
            ),
            (["to"], {"help": "address to which the tx was sent (0x...)"}),
            (["-d", "--desc"], {"action": "store"}),
            (
                ["-u", "--update"],
                {
                    "help": "if a transaction with the same hash is present, overwrite it",
                    "action": "store_true",
                },
            ),
            args.chain(),
        ],
    )
    def add(self) -> None:
        tx = Tx.get_by_hash(self.app.pargs.hash)
        if not tx or self.app.pargs.update:
            Tx.upsert(
                {
                    "hash": self.app.pargs.hash,
                    "chain": self.app.chain.name,
                    "from_": getattr(self.app.pargs, "from"),
                    "to": self.app.pargs.to,
                    "desc": self.app.pargs.desc,
                },
                logger=self.app.log.info,
            )
        else:
            raise Web3CliError(
                f"Transaction '{self.app.pargs.hash}' already exists. Use `--update` or `-u` to update it."
            )

    @ex(
        help="delete a transaction from the history",
        arguments=[
            (["hash"], {"help": "hash of the tx to delete"}),
        ],
    )
    def delete(self) -> None:
        tx = Tx.get_by_hash_or_raise(self.app.pargs.hash)
        tx.delete_instance()
        self.app.log.info(f"Transaction '{self.app.pargs.hash}' deleted correctly")
