import web3
from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.args import parse_block
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_client
from web3core.helpers.abi import parse_abis
from web3core.helpers.resolve import resolve_address


class CallController(Controller):
    """Handler of the `w3 call` top-level commands"""

    class Meta:
        label = "call"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Call a function in the given smart contract, using eth_call. To see the list of functions, use `w3 abi functions`.",
        arguments=[
            (["contract"], {"action": "store"}),
            (["function"], {"action": "store"}),
            (["args"], {"action": "store", "nargs": "*"}),
            (["-b", "--block"], args.block()),
        ],
    )
    def call(self) -> None:
        chain_ready_or_raise(self.app)
        # Try to fetch the function from the ABI
        client = make_contract_client(self.app, self.app.pargs.contract)
        functions = client.functions
        try:
            function = functions[self.app.pargs.function]
        except web3.exceptions.ABIFunctionNotFound:
            raise Web3CliError(f"Function must be one of: {', '.join(functions)}")
        # Parse block identifier
        block = parse_block(self.app, "block")
        # Parse function args
        function_args = parse_abis(
            self.app.pargs.args,
            client.contract.abi,
            self.app.pargs.function,
            checksum_addresses=True,
            resolve_address_fn=lambda x: resolve_address(x, chain=self.app.chain_name),
            allow_exp_notation=True,
        )
        # Call the function
        result = function(*function_args).call(block_identifier=block)
        self.app.render(result, indent=4, handler="json")
