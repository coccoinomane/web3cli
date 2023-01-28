from typing import Any, List

import web3
from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_client
from web3core.exceptions import NotSupportedYet
from web3core.helpers.abi import get_function_abi, parse_abi_value
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
            (
                ["-b", "--block"],
                {
                    "action": "store",
                    "help": "Block identifier. Can be a block number, a hash, or one of the following: latest, earliest, pending, safe, finalized",
                    "default": "latest",
                },
            ),
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
        # Convert the args passed from the command line into python arguments compatible
        # with the contract function's ABI
        function_abis = get_function_abi(client.contract.abi, self.app.pargs.function)
        if len(function_abis) > 1:
            raise NotSupportedYet(
                f"The contract has {len(function_abis)} overloaded functions for {self.app.pargs.function}. This is not supported yet."
            )
        function_abi = function_abis[0]
        # Check that the number of args passed from the command line is correct
        function_inputs = function_abi["inputs"]
        if len(function_inputs) != len(self.app.pargs.args):
            raise Web3CliError(
                f"Function {self.app.pargs.function} expects {len(function_inputs)} arguments, but {len(self.app.pargs.args)} were given"
            )
        # Loop over the function's inputs and convert the args passed from the
        # command line
        converted_args: List[Any] = []
        for i, input in enumerate(function_inputs):
            string_value = self.app.pargs.args[i]
            abi_name = input["name"]
            abi_type = input["type"]
            try:
                converted_value = parse_abi_value(
                    abi_type,
                    string_value,
                    resolve_address_fn=lambda x: resolve_address(
                        x, chain=self.app.chain_name
                    ),
                    allow_exp_notation=True,
                )
                converted_args.append(converted_value)
            except TypeError:
                raise Web3CliError(
                    f"Argument '{abi_name}' expects type '{abi_type}', but received value '{string_value}' could not be converted"
                )
        # Parse block identifier
        try:
            block = int(self.app.pargs.block)
        except ValueError:
            block = self.app.pargs.block
        # Call the function
        result = function(*converted_args).call(block_identifier=block)
        self.app.render(result, indent=4, handler="json")
