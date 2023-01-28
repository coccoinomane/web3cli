import csv
from typing import Any, Callable, List, Union, cast

import web3
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
from web3.types import ABI, ABIEvent, ABIFunction

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


def get_function_abi(abi: ABI, name: str) -> List[ABIFunction]:
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
    abi_type: str,
    string_value: str,
    checksum_addresses: bool = True,
    resolve_address_fn: Callable[[str], str] = lambda x: x,
    allow_exp_notation: bool = True,
) -> Any:
    """Convert an ABI value from a string to a python type.

    For array types, the string value must be a comma-separated
    list of values; to use spaces or commas in a value, enclose
    it in double quotes.

    Args:
        abi_type: The ABI type of the value to convert.
        string_value: The value to convert.
        checksum_addresses: Whether to convert addresses to checksum addresses.
        resolve_address_fn: A function to resolve addresses from strings.
        allow_exp_notation: Whether to allow exponential notation for integers
        (e.g. 5e18 will be translated to 5000000000000000000).
    """
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
        raise NotSupportedYet("Bytes type is not supported yet")
    elif is_string_type(abi_type):
        value = str(string_value)
    elif is_address_type(abi_type):
        value = resolve_address_fn(string_value)
        if checksum_addresses:
            value = web3.Web3.toChecksumAddress(value)
    elif is_array_type(abi_type):
        sub_type = sub_type_of_array_type(abi_type)
        csv_reader = csv.reader([string_value], skipinitialspace=True)
        value = [
            parse_abi_value(
                sub_type, v, checksum_addresses, resolve_address_fn, allow_exp_notation
            )
            for v in next(csv_reader)
        ]
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

    validate_abi_value(abi_type, value)

    return value


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


def _inputs(abi: Union[ABIFunction, ABIEvent]) -> str:
    types_list = get_type_strings(abi["inputs"])
    params = zip([i["name"] for i in abi["inputs"]], types_list)
    return ", ".join(f"{i[1]}{' '+i[0] if i[0] else ''}" for i in params)
