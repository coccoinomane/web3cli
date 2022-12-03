from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.models.tx import Tx
from web3cli.core.exceptions import TxIsInvalid, Web3CliError
from web3cli.helpers.render import render_table
from web3cli.core.helpers.format import cut
from playhouse.shortcuts import model_to_dict


class TxController(Controller):
    """Handler of the `w3 db tx` commands"""

    class Meta:
        label = "tx"
        help = "add, list or delete transactions"
        stacked_type = "nested"
        stacked_on = "db"

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
        self.app.render(model_to_dict(tx))

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
            (["-d", "--description"], {"action": "store"}),
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
        if not Tx.is_valid_hash(self.app.pargs.hash):
            raise TxIsInvalid(f"Invalid transaction hash given: {self.app.pargs.hash}")
        tx = Tx.get_by_hash(self.app.pargs.hash)
        if not tx or self.app.pargs.update:
            Tx.upsert(
                {
                    "hash": self.app.pargs.hash,
                    "chain": self.app.chain,
                    "from_": getattr(self.app.pargs, "from"),
                    "to": self.app.pargs.to,
                    "description": self.app.pargs.description,
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
