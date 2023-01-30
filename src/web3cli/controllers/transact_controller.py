import json

import web3
from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.helpers.abi import parse_abi_values
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address


class TransactController(Controller):
    """Handler of the `w3 transact` top-level commands"""

    class Meta:
        label = "transact"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Execute a function in the given smart contract and, by default, return the transaction hash. This will cost gas and write to the blockchain. Please use `w3 send` if you just need to send tokens around, as it is less error prone. To see the list of functions in a given contract, run `w3 abi functions <contract>`.",
        arguments=[
            (["contract"], {"action": "store"}),
            (["function"], {"action": "store"}),
            (["args"], {"action": "store", "nargs": "*"}),
            (
                ["-o", "--output"],
                {
                    "action": "store",
                    "help": "What should be printed after the command has been executed.",
                    "choices": ["hash", "tx", "sig", "receipt", "rcpt"],
                    "default": "hash",
                },
            ),
            (
                ["--dry-run"],
                {
                    "action": "store_true",
                    "help": "If set, the transaction will not be sent. Useful to print the transaction data and check that it is correct.",
                },
            ),
            (["-f", "--force"], args.force()),
        ],
        aliases=["exec"],
    )
    def transact(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        # Try to fetch the function from the ABI
        client = make_contract_wallet(self.app, self.app.pargs.contract)
        functions = client.functions
        try:
            function = functions[self.app.pargs.function]
        except web3.exceptions.ABIFunctionNotFound:
            raise Web3CliError(f"Function must be one of: {', '.join(functions)}")
        # Parse function args
        function_args, input_names = parse_abi_values(
            self.app.pargs.args,
            client.contract.abi,
            self.app.pargs.function,
            checksum_addresses=True,
            resolve_address_fn=lambda x: resolve_address(x, chain=self.app.chain_name),
            allow_exp_notation=True,
        )
        # Build transaction
        tx = client.buildContractTransaction(function(*function_args))
        # Sign transaction
        tx_signed = client.signTransaction(tx)
        # Ask for confirmation
        if not self.app.pargs.force and not self.app.pargs.dry_run:
            print(
                f"You are about to execute '{self.app.pargs.function}' on contract '{self.app.pargs.contract}' on the {self.app.chain.name} chain with the following arguments:"
            )
            for i, arg in enumerate(function_args):
                print(f"  {input_names[i]}: {arg}")
            yes_or_exit(logger=self.app.log.info)
        # Send transaction
        if not self.app.pargs.dry_run:
            tx_hash = client.sendSignedTransaction(tx_signed)
        else:
            tx_hash = tx_signed.hash.hex()
        # Print output
        if self.app.pargs.output == "hash":
            self.app.render(tx_hash, indent=4, handler="json")
        elif self.app.pargs.output == "tx":
            self.app.render(tx, indent=4, handler="json")
        elif self.app.pargs.output == "sig":
            self.app.render(
                json.loads(Web3.toJSON(tx_signed._asdict())), indent=4, handler="json"
            )
        elif self.app.pargs.output in ["receipt", "rcpt"]:
            rcpt = client.getTransactionReceipt(tx_hash)
            self.app.render(json.loads(Web3.toJSON(rcpt)), indent=4, handler="json")
        else:
            raise Web3CliError(f"Unknown output type: {self.app.pargs.output}")
