import json

from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client


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
        tx_as_dict = json.loads(Web3.to_json(tx))
        self.app.render(tx_as_dict, indent=4, handler="json")

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
        receipt_as_dict = json.loads(Web3.to_json(receipt))
        self.app.render(receipt_as_dict, indent=4, handler="json")
