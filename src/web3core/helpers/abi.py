from typing import Any, List, Union, cast

from web3._utils.abi import abi_to_signature, filter_by_name, filter_by_type
from web3.types import ABI, ABIEvent, ABIFunction

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
