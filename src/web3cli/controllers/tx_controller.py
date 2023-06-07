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
            (
                ["--fee-multiplier"],
                {
                    "help": "multiply gas price by this factor with respect to the original tx; set to zero to estimate it based on current chain conditions",
                    "default": 0,
                    "type": float,
                },
            ),
            (
                ["--gas-multiplier"],
                {
                    "help": "multiply the gas limit by this factor with respect to the gas spent by the original tx",
                    "default": 1.2,
                    "type": float,
                },
            ),
            (
                ["--type"],
                {"help": "Override the type of the original tx", "type": int},
            ),
            args.force(),
        ],
    )
    def replay(self) -> None:
        original_tx = make_client(self.app).get_tx(self.app.pargs.hash)
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
        if original_tx.get("type"):
            tx["type"] = original_tx["type"]
        # Make sure you use the right amount of gas
        tx["gas"] = int(int(original_tx["gas"]) * self.app.pargs.gas_multiplier)
        # For post EIP-1559 transactions, use the same tip and max gas
        if self.app.pargs.fee_multiplier != 0 and original_tx.get("maxFeePerGas"):
            tx["maxFeePerGas"] = int(
                original_tx["maxFeePerGas"] * self.app.pargs.fee_multiplier
            )
        if self.app.pargs.fee_multiplier != 0 and original_tx.get(
            "maxPriorityFeePerGas"
        ):
            tx["maxPriorityFeePerGas"] = int(
                original_tx["maxPriorityFeePerGas"] * self.app.pargs.fee_multiplier
            )
        # For pre EIP-1559 transactions, use the same gas price
        if (
            self.app.pargs.fee_multiplier != 0
            and original_tx.get("gasPrice")
            and not original_tx.get("maxFeePerGas")
            and not original_tx.get("maxPriorityFeePerGas")
        ):
            tx["gasPrice"] = int(
                original_tx["gasPrice"] * self.app.pargs.fee_multiplier
            )
        # Optionally override type field
        if self.app.pargs.type is not None:
            tx["type"] = self.app.pargs.type
        # Ask for confirmation
        if not self.app.pargs.force:
            self.app.log.info(f"Replaying the following transaction:")
            render_web3py(self.app, original_tx)
            print("\n")
            self.app.log.info(f"Transaction that will be sent:")
            render_web3py(self.app, tx)
            print("\n")
            yes_or_exit("Continue? ")
        # Send transaction
        try:
            tx_hash = signer.sign_and_send_tx(tx)
        except TypeError as e:
            raise Web3CliError(
                f"Failed to send transaction: {e}. "
                f"Try using the flag --type {self.app.chain.tx_type} to prevent type-related errors."
            )
        self.app.print(tx_hash)
