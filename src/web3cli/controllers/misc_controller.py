import json
from pprint import pformat
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
from web3cli.helpers.client_factory import (
    make_client,
    make_contract_client,
    make_wallet,
)
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.exceptions import NotSupportedYet
from web3core.helpers.abi import get_function_abi
from web3core.helpers.misc import to_bool
from web3core.helpers.resolve import resolve_address


class MiscController(Controller):
    """Handler of simple top-level commands"""

    class Meta:
        label = "misc"
        help = "simple top-level commands"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Get the balance of the given address in the blockchain coin (ETH, BNB, AVAX, etc)",
        arguments=[(["address"], {"action": "store"})],
    )
    def balance(self) -> None:
        chain_ready_or_raise(self.app)
        balance = make_client(self.app).getBalanceInEth(
            resolve_address(self.app.pargs.address, chain=self.app.chain_name)
        )
        self.app.render(
            {"amount": balance, "ticker": self.app.chain.coin},
            "balance.jinja2",
            handler="jinja2",
        )

    @ex(
        help="Get the latest block, or the block corresponding to the given identifier",
        arguments=[
            (
                ["block_identifier"],
                {
                    "help": "Block identifier. Can be a block number, an hash, or one of the following: latest, earliest, pending, safe, finalized",
                    "nargs": "?",
                    "default": "latest",
                },
            )
        ],
    )
    def block(self) -> None:
        chain_ready_or_raise(self.app)
        block = None
        client = make_client(self.app)
        # In case a block number was given
        try:
            block = client.w3.eth.get_block(int(self.app.pargs.block_identifier))
        except ValueError:
            pass
        # In case a string
        if not block:
            block = client.w3.eth.get_block(self.app.pargs.block_identifier)
        block_as_dict = json.loads(web3.Web3.toJSON(block))
        self.app.render(block_as_dict, indent=4, handler="json")

    @ex(
        help="Sign the given message and show the signed message, as returned by web3.py",
        arguments=[(["msg"], {"action": "store"})],
    )
    def sign(self) -> None:
        signer_ready_or_raise(self.app)
        signed_message = make_wallet(self.app).signMessage(self.app.pargs.msg)
        self.app.print(pformat(signed_message._asdict()))

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
