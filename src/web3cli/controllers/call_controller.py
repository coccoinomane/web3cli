from typing import Any, Callable, List

import web3
from cement import ex
from web3._utils.abi import (
    is_address_type,
    is_array_type,
    is_bool_type,
    is_bytes_type,
    is_int_type,
    is_string_type,
    is_uint_type,
    sub_type_of_array_type,
)
from web3._utils.validation import validate_abi_value

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_client
from web3core.exceptions import NotSupportedYet
from web3core.helpers.abi import get_function_abi
from web3core.helpers.misc import to_bool
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
                converted_value = _convert_string_value(
                    abi_type,
                    string_value,
                    resolve_address_fn=lambda x: resolve_address(
                        x, chain=self.app.chain_name
                    ),
                )
                converted_args.append(converted_value)
            except TypeError:
                raise Web3CliError(
                    f"Argument '{abi_name}' expects type '{abi_type}', but received value '{string_value}' could not be converted"
                )
        # Call the function
        result = function(*converted_args).call()
        self.app.print(str(result))


def _convert_string_value(
    abi_type: str,
    string_value: str,
    checksum_addresses: bool = True,
    resolve_address_fn: Callable[[Any], str] = lambda x: x,
) -> Any:
    """Convert an ABI value from a string to a python type"""
    value: Any = None
    if is_bool_type(abi_type):
        value = to_bool(string_value)
    elif is_int_type(abi_type):
        value = int(string_value)
    elif is_uint_type(abi_type):
        value = int(string_value)
    elif is_bytes_type(abi_type):
        raise NotSupportedYet("Bytes type is not supported yet")
    elif is_string_type(abi_type):
        value = str(string_value)
    elif is_address_type(abi_type):
        value = resolve_address_fn(string_value)
        if checksum_addresses:
            value = web3.Web3.toChecksumAddress(value)
    elif is_array_type(abi_type):
        sub_type = sub_type_of_array_type(abi_type)
        value = [
            _convert_string_value(sub_type, v, checksum_addresses, resolve_address_fn)
            for v in string_value.split(",")
        ]
    else:
        raise Web3CliError(f"Unsupported ABI type: {abi_type}")

    validate_abi_value(abi_type, value)

    return value
