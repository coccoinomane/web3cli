from cement import ex
from playhouse.shortcuts import model_to_dict

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers.render import render_table
from web3core.helpers.format import cut
from web3core.models.tx import Tx


class DbTxController(Controller):
    """Handler of the `w3 db tx` commands"""

    class Meta:
        label = "trx"  # trx instead of tx to avoid conflict with TxController
        help = "add, list or delete transactions"
        stacked_type = "nested"
        stacked_on = "db"
        aliases = ["tx"]

    @ex(help="list transactions")
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
        help="show details of the given transaction",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
        ],
    )
    def get(self) -> None:
        tx = Tx.get_by_hash_or_raise(self.app.pargs.hash)
        self.app.render(model_to_dict(tx), indent=4, handler="json")

    @ex(
        help="add a new transaction to the database",
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
        ],
    )
    def add(self) -> None:
        tx = Tx.get_by_hash(self.app.pargs.hash)
        if not tx or self.app.pargs.update:
            Tx.upsert(
                {
                    "hash": self.app.pargs.hash,
                    "chain": self.app.chain_name,
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
        help="delete a transaction",
        arguments=[
            (["hash"], {"help": "hash of the tx to delete"}),
        ],
    )
    def delete(self) -> None:
        tx = Tx.get_by_hash_or_raise(self.app.pargs.hash)
        tx.delete_instance()
        self.app.log.info(f"Transaction '{self.app.pargs.hash}' deleted correctly")
