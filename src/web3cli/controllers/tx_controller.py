from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client
from web3cli.helpers.render import render


class TxController(Controller):
    """Handler of the `w3 tx` commands"""

    class Meta:
        label = "tx"
        help = "fetch transactions from the blockchain"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="fetch the given transaction from the blockchain",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            *args.chain_and_rpc(),
        ],
    )
    def get(self) -> None:
        client = make_client(self.app)
        tx = client.w3.eth.get_transaction(self.app.pargs.hash)
        render(self.app, tx)

    @ex(
        help="fetch the receipt of the given transaction from the blockchain",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            *args.chain_and_rpc(),
        ],
        aliases=["rc"],
    )
    def get_receipt(self) -> None:
        client = make_client(self.app)
        receipt = client.w3.eth.wait_for_transaction_receipt(self.app.pargs.hash)
        render(self.app, receipt)
