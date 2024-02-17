import binascii
import csv
from typing import Any, Callable, Dict, List, Tuple, Union, cast

from eth_utils import encode_hex, function_abi_to_4byte_selector
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import (
    abi_to_signature,
    filter_by_name,
    filter_by_type,
    is_address_type,
    is_array_type,
    is_bool_type,
    is_bytes_type,
    is_int_type,
    is_string_type,
    is_uint_type,
    size_of_type,
    sub_type_of_array_type,
)
from web3._utils.validation import validate_abi_value
from web3.types import ABI, ABIEvent, ABIFunction, ABIFunctionParams

from web3cli.exceptions import Web3CliError
from web3core.exceptions import AbiOverflow, NotSupportedYet
from web3core.helpers.misc import to_bool, to_int

#  _____                          _     _
# |  ___|  _   _   _ __     ___  | |_  (_)   ___    _ __    ___
# | |_    | | | | | '_ \   / __| | __| | |  / _ \  | '_ \  / __|
# |  _|   | |_| | | | | | | (__  | |_  | | | (_) | | | | | \__ \
# |_|      \__,_| |_| |_|  \___|  \__| |_|  \___/  |_| |_| |___/


def get_function_names(abi: ABI) -> List[str]:
    """Given an ABI, return the names of its function"""
    return [f["name"] for f in filter_abi_by_type_and_name(abi, "function")]


def get_function_signatures(abi: ABI) -> List[str]:
    """Given an ABI, return the signatures of its function"""
    return [abi_to_signature(f) for f in filter_abi_by_type_and_name(abi, "function")]


def get_function_full_signatures(abi: ABI) -> List[str]:
    """Given an ABI, return the signatures of its function, including
    the argument names"""
    return [
        f"{abi['name']}({_inputs(abi)})"
        for abi in filter_abi_by_type_and_name(abi, "function")
    ]


def get_function_abis(abi: ABI, name: str) -> List[ABIFunction]:
    """Given an ABI, return the ABIs of the functions with the given name"""
    return cast(List[ABIFunction], filter_abi_by_type_and_name(abi, "function", name))


#  _____                          _
# | ____| __   __   ___   _ __   | |_   ___
# |  _|   \ \ / /  / _ \ | '_ \  | __| / __|
# | |___   \ V /  |  __/ | | | | | |_  \__ \
# |_____|   \_/    \___| |_| |_|  \__| |___/


def get_event_names(abi: ABI) -> List[str]:
    """Given an ABI, return the names of its event"""
    return [f["name"] for f in filter_abi_by_type_and_name(abi, "event")]


def get_event_signatures(abi: ABI) -> List[str]:
    """Given an ABI, return the signatures of its event"""
    return [abi_to_signature(f) for f in filter_abi_by_type_and_name(abi, "event")]


def get_event_full_signatures(abi: ABI) -> List[str]:
    """Given an ABI, return the signatures of its event, including
    the parameter names"""
    return [
        f"{abi['name']}({_inputs(abi)})"
        for abi in filter_abi_by_type_and_name(abi, "event")
    ]


def get_event_abi(abi: ABI, name: str) -> List[ABIEvent]:
    """Given an ABI, return the ABIs of the events with the given name"""
    return cast(List[ABIEvent], filter_abi_by_type_and_name(abi, "event", name))


#  _   _   _     _   _
# | | | | | |_  (_) | |  ___
# | | | | | __| | | | | / __|
# | |_| | | |_  | | | | \__ \
#  \___/   \__| |_| |_| |___/


def filter_abi_by_type_and_name(abi: ABI, type: str = None, name: str = None) -> ABI:
    """Given an ABI, return the list of ABIs therein contained, filtered by
    type and name. If type is None, all types are returned. If name is None,
    all names are returned. If both are None, the whole ABI is returned.

    Please note that a function can apper more than once with the
    same name but different sets of arguments."""
    if type is not None:
        abi = filter_by_type(type, abi)
    if name is not None:
        abi = filter_by_name(name, abi)
    return abi


def parse_abi_value(
    string_value: str,
    abi_type: str = None,
    abi_input: ABIFunctionParams = None,
    checksum_addresses: bool = True,
    resolve_address_fn: Callable[[str], str] = lambda x: x,
    allow_exp_notation: bool = True,
) -> Any:
    """Convert an ABI value from a string to a python type.

    For iterable types (lists, arrays tuples), please use the
    `parse_iterable_abi_value` function.

    Args:
        abi_type: The ABI type of the value to convert, e.g. `string` or
        `tuple`.
        string_value: The value to convert.
        abi_input: The full ABI inuput dictionary for this argument, if
            available.  It is required only for parsing a tuple, so that the
            function can access its `components`. checksum_addresses: Whether
            to convert addresses to checksum addresses.
        resolve_address_fn: A function to resolve addresses from strings.
        allow_exp_notation: Whether to allow exponential notation for integers
            (e.g. 5e18 will be translated to 5000000000000000000).
    """
    if abi_type is None and abi_input is None:
        raise ValueError("Either abi_type or abi_input must be provided")
    if abi_input:
        abi_type = abi_input["type"]
    value: Any = None
    if is_bool_type(abi_type):
        value = to_bool(string_value)
    elif is_int_type(abi_type):
        if string_value.startswith("0x"):
            raise NotSupportedYet("Hexadecimal integers are not supported yet")
        value = to_int(string_value, allow_exp_notation)
    elif is_uint_type(abi_type):
        if string_value.startswith("0x"):
            raise NotSupportedYet("Hexadecimal integers are not supported yet")
        value = to_int(string_value, allow_exp_notation)
        if value < 0:
            raise ValueError("Unsigned integers must be positive")
    elif is_bytes_type(abi_type):
        try:
            value = HexBytes(string_value)
        except binascii.Error as e:
            raise Web3CliError(
                f"Value '{string_value}' is not a valid hex string ({e})"
            )
    elif is_string_type(abi_type):
        value = str(string_value)
    elif is_address_type(abi_type):
        value = resolve_address_fn(string_value)
        if checksum_addresses:
            value = Web3.to_checksum_address(value)
    elif is_array_type(abi_type):
        sub_type = sub_type_of_array_type(abi_type)
        if is_array_type(sub_type):
            raise NotSupportedYet("Nested arrays are not supported yet.")
        csv_reader = csv.reader([string_value], skipinitialspace=True)
        value = [
            parse_abi_value(
                string_value=v,
                abi_type=sub_type,
                checksum_addresses=checksum_addresses,
                resolve_address_fn=resolve_address_fn,
                allow_exp_notation=allow_exp_notation,
            )
            for v in next(csv_reader)
        ]
    elif abi_type == "tuple":
        if abi_input is None:
            raise ValueError(
                "The full ABI input dictionary is required to parse a tuple"
            )
        sub_names = [c["name"] for c in abi_input["components"]]
        sub_types = [c["type"] for c in abi_input["components"]]
        sub_args = list(csv.reader([string_value], skipinitialspace=True))[0]
        if len(sub_args) != len(sub_types):
            raise Web3CliError(
                f"Provided {len(sub_args)} values for tuple argument {abi_input['name']}, expected {len(sub_types)}.  You provided {sub_args}, expected {sub_types}."
            )
        value = {}
        for i, sub_arg in enumerate(sub_args):
            if sub_types[i] == "tuple":
                raise NotSupportedYet("Tuple of tuples not supported")
            if is_array_type(sub_types[i]):
                raise NotSupportedYet("Tuple of arrays not supported")
            sub_key = sub_names[i]
            value[sub_key] = parse_abi_value(
                string_value=sub_arg,
                abi_type=sub_types[i],
                checksum_addresses=checksum_addresses,
                resolve_address_fn=resolve_address_fn,
                allow_exp_notation=allow_exp_notation,
            )
    else:
        raise Web3CliError(f"Unsupported ABI type: {abi_type}")

    # Check that the value is not too big for the type
    if is_int_type(abi_type) or is_uint_type(abi_type):
        size = size_of_type(abi_type)  # 256 for uint256, 8 for uint8, etc.
        max_int = 2 ** (size if is_uint_type(abi_type) else size - 1)
        if abs(value) >= max_int:
            raise AbiOverflow(
                f"Value {string_value} is too big for type {abi_type}, "
                f"max value is {max_int - 1}"
            )

    # Check that the value is valid for the type (tuple not supported)
    if abi_type != "tuple":
        validate_abi_value(abi_type, value)

    return value


def parse_abi_values(
    args: List[str],
    contract_abi: ABI,
    function: str,
    checksum_addresses: bool = True,
    resolve_address_fn: Callable[[str], str] = lambda x: x,
    allow_exp_notation: bool = True,
) -> Tuple[List[Any], List[str]]:
    """Cast strings to python arguments for the given contract
    function.

    This is basically a loop of parse_abi calls, with some
    additional checks.

    Returns:
        A tuple with the converted arguments and the names of the
        arguments.
    """
    # Check that the function is contained in the ABI
    function_abis = get_function_abis(contract_abi, function)
    if len(function_abis) > 1:
        raise NotSupportedYet(
            f"The contract has {len(function_abis)} overloaded functions for {function}. This is not supported yet."
        )
    elif len(function_abis) == 0:
        raise Web3CliError(f"Function {function} not found in the ABI")

    # Check that the number of args passed from the command line is correct
    function_abi = function_abis[0]
    function_inputs = function_abi["inputs"]
    if len(function_inputs) != len(args):
        raise Web3CliError(
            f"Function {function} expects {len(function_inputs)} arguments, but {len(args)} were given"
        )
    # Convert the string list into python arguments for the function
    converted_args: List[Any] = []
    for i, abi_input in enumerate(function_inputs):
        string_value = args[i]
        try:
            converted_value = parse_abi_value(
                string_value=string_value,
                abi_input=abi_input,
                checksum_addresses=checksum_addresses,
                resolve_address_fn=resolve_address_fn,
                allow_exp_notation=allow_exp_notation,
            )
            converted_args.append(converted_value)
        except TypeError as e:
            raise Web3CliError(
                f"Argument '{abi_input['name']}' expects type '{abi_input['type']}', but received value '{string_value}' could not be converted.  TypeError: {e}"
            )
    return (converted_args, [i["name"] for i in function_inputs])


def get_type_strings(abi_params: Any) -> List[str]:
    """Converts a list of parameters from an ABI into a list of type strings.
    Source: Brownie"""
    types_list = []

    for i in abi_params:
        if i["type"].startswith("tuple"):
            params = get_type_strings(i["components"])  # cast to avoid mypy error
            array_size = i["type"][5:]
            types_list.append(f"({','.join(params)}){array_size}")
        else:
            type_str = i["type"]
            types_list.append(type_str)

    return types_list


def does_function_write_to_state(abi: ABIFunction) -> bool:
    """Returns True if the function writes to the state, False otherwise."""
    return abi["stateMutability"] not in ("view", "pure")


def _inputs(abi: Union[ABIFunction, ABIEvent]) -> str:
    """Private helper function"""
    types_list = get_type_strings(abi["inputs"])
    params = zip([i["name"] for i in abi["inputs"]], types_list)
    return ", ".join(f"{i[1]}{' '+i[0] if i[0] else ''}" for i in params)


def decode_function_data(
    abi: ABI, data: str, name: str = None
) -> Tuple[Dict[str, Any], str]:
    """Given input data for a contract function, return the
    decoded arguments and the signature of the function"""
    web3_contract = Web3().eth.contract(abi=abi)
    # Prepend selector if function name is specified
    if name:
        try:
            func_obj = web3_contract.get_function_by_name(name)
        except ValueError as e:
            raise Web3CliError(f"Could not find function {name}: {e}")
        selector = encode_hex(function_abi_to_4byte_selector(func_obj.abi))
        if not data.startswith(selector):
            data = selector + data
    # Decode the function params
    try:
        func_obj, func_params = web3_contract.decode_function_input(data)
    except ValueError as e:
        raise Web3CliError(f"Could not decode function input: {e}")
    return func_params, abi_to_signature(func_obj.abi)
