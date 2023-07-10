import web3
from cement import ex

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.args import parse_block
from web3cli.helpers.client_factory import make_contract_client
from web3cli.helpers.render import render
from web3core.helpers.abi import (
    does_function_write_to_state,
    get_function_abis,
    parse_abi_values,
)
from web3core.helpers.resolve import resolve_address


class CallController(Controller):
    """Handler of the `w3 call` top-level commands"""

    class Meta:
        label = "call"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Simulate calling a function in the given smart contract using eth_call, and return the function output. This will not cost gas nor write to the blockchain. To see the list of functions in a given contract, run `w3 abi functions <contract>`.",
        arguments=[
            (["contract"], {"action": "store"}),
            (["function"], {"action": "store"}),
            (["args"], {"action": "store", "nargs": "*"}),
            args.block(),
            (
                ["--from"],
                {
                    "dest": "from_",
                    "help": "From address.  Needed when simulating write operations, e.g. a swap or a token transfer.",
                },
            ),
            *args.chain_and_rpc(),
        ],
    )
    def call(self) -> None:
        # Get client to interact with the chain
        client = make_contract_client(self.app, self.app.pargs.contract)

        # Try to fetch the function from the ABI
        functions = client.functions
        try:
            function = functions[self.app.pargs.function]
        except web3.exceptions.ABIFunctionNotFound:
            raise Web3CliError(f"Function must be one of: {', '.join(functions)}")

        # If the function is a write operation, we need a from address
        from_address = None
        fn_abi = get_function_abis(client.contract.abi, self.app.pargs.function)[0]
        if does_function_write_to_state(fn_abi):
            if self.app.pargs.from_ is None:
                raise Web3CliError("Please specify a from address with --from")
            else:
                from_address = resolve_address(self.app.pargs.from_)

        # Parse block identifier
        block = parse_block(self.app, "block")

        # Parse function args
        function_args, _ = parse_abi_values(
            self.app.pargs.args,
            client.contract.abi,
            self.app.pargs.function,
            checksum_addresses=True,
            resolve_address_fn=lambda x: resolve_address(x, chain=self.app.chain.name),
            allow_exp_notation=True,
        )

        # Call the function
        if from_address is None:
            result = function(*function_args).call(block_identifier=block)
        else:  # from address needed
            result = function(*function_args).call(
                {"from": from_address}, block_identifier=block
            )
        render(self.app, result)
