import argparse
import json

from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_client, make_wallet
from web3cli.helpers.render import render_web3py
from web3core.helpers.misc import yes_or_exit


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

    @ex(
        help="replay the given transaction on the blockchain",
        arguments=[
            (["hash"], {"help": "hash of the transaction"}),
            *args.chain_and_rpc(),
            args.signer(),
            args.priority_fee(
                help="Optionally override priority fee, in gwei", default=None
            ),
            (
                ["--preserve-type", "-p"],
                {
                    "help": "Whether to preserve the transaction type.  Disable on zkSync.",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
            args.tx_gas_limit(help="Optionally override gas limit"),
            args.force(),
        ],
    )
    def replay(self) -> None:
        original_tx = make_client(self.app).get_tx(self.app.pargs.hash)
        # Ask for confirmation
        if not self.app.pargs.force:
            self.app.log.info(f"Replaying the following transaction:")
            render_web3py(self.app, original_tx)
            yes_or_exit("\nContinue? ")
        # Build replay transaction
        signer = make_wallet(self.app)
        tx = signer.build_base_tx()
        # Make sure you call the same contract
        tx["to"] = original_tx["to"]
        # Make sure you call the same method with same args
        if original_tx.get("input"):
            tx["data"] = original_tx["input"]
        # Make sure you pay the same amount
        tx["value"] = original_tx["value"]
        # Make sure you send the same type of transaction
        if self.app.pargs.preserve_type and original_tx.get("type"):
            tx["type"] = original_tx["type"]
        # Make sure you use the same gas limit
        tx["gas"] = original_tx["gas"]
        # For post EIP-1559 transactions, use the same tip and max gas
        if original_tx.get("maxFeePerGas"):
            tx["maxFeePerGas"] = original_tx["maxFeePerGas"]
        if original_tx.get("maxPriorityFeePerGas"):
            tx["maxPriorityFeePerGas"] = original_tx["maxPriorityFeePerGas"]
        # For pre EIP-1559 transactions, use the same gas price
        if (
            original_tx.get("gasPrice")
            and not original_tx.get("maxFeePerGas")
            and not original_tx.get("maxPriorityFeePerGas")
        ):
            tx["gasPrice"] = original_tx["gasPrice"]
        # Optionally override original gas settings
        if self.app.pargs.gas_limit:
            tx["gas"] = self.app.pargs.gas_limit
        if self.app.pargs.priority_fee:
            tx["maxPriorityFeePerGas"] = Web3.to_wei(
                self.app.pargs.priority_fee, "gwei"
            )
        # Send transaction
        try:
            tx_hash = signer.sign_and_send_tx(tx)
        except TypeError as e:
            raise Web3CliError(
                f"Failed to send transaction: {e}. "
                f"Try using --no-preserve-type to disable transaction type preservation."
            )
        self.app.print(tx_hash)
