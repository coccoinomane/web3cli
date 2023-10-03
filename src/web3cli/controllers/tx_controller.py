from cement import ex
from web3 import Web3
from web3.datastructures import AttributeDict
from web3client.helpers.tx import parse_raw_tx

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
        help="Fetch the given transaction from the blockchain",
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
        help="Fetch the receipt of the given transaction from the blockchain",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            *args.chain_and_rpc(),
        ],
        aliases=["rc", "receipt"],
    )
    def get_receipt(self) -> None:
        client = make_client(self.app)
        receipt = client.w3.eth.wait_for_transaction_receipt(self.app.pargs.hash)
        render(self.app, receipt)

    @ex(
        help="Decode a raw transaction",
        arguments=[(["raw_tx"], {"help": "Raw transaction to decode in hex format"})],
        aliases=["parse-raw-tx"],
    )
    def parse_raw(self) -> None:
        decoded_tx = parse_raw_tx(self.app.pargs.raw_tx)
        render(self.app, AttributeDict(decoded_tx))

    @ex(
        help="Fetch the given transaction from the blockchain, and show it in its raw hex form.  Plese note that not all RPCs support this method (e.g. Pokt and Ankr do, Infura and Cloudfare do not).",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            *args.chain_and_rpc(),
        ],
        aliases=["raw"],
    )
    def get_raw(self) -> None:
        client = make_client(self.app)
        raw_tx = client.w3.eth.get_raw_transaction(self.app.pargs.hash)
        render(self.app, Web3.to_hex(raw_tx))
