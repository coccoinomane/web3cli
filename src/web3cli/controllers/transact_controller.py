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
from web3core.helpers.tx import send_contract_transaction


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
            (["-o", "--output"], args.tx_output()),
            (["--dry-run"], args.tx_dry_run()),
            (["-f", "--force"], args.force()),
        ],
        aliases=["exec"],
    )
    def transact(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        # Parse args
        dry_run, output_type = args.parse_dry_run_and_tx_output(self.app)
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
        # Ask for confirmation
        if not self.app.pargs.force and not dry_run:
            print(
                f"You are about to execute '{self.app.pargs.function}' on contract '{self.app.pargs.contract}' on the {self.app.chain.name} chain with the following arguments:"
            )
            for i, arg in enumerate(function_args):
                print(f"  {input_names[i]}: {arg}")
            yes_or_exit(logger=self.app.log.info)
        # Send transaction
        output = send_contract_transaction(
            client,
            function(*function_args),
            dry_run=dry_run,
            output_type=output_type,
            maxPriorityFeePerGasInGwei=self.app.priority_fee,
        )
        # Print output
        self.app.render(json.loads(Web3.toJSON(output)), indent=4, handler="json")
