from typing import cast

import pytest
from hexbytes import HexBytes
from web3.exceptions import InvalidAddress
from web3.types import ABI, ABIFunctionParams

from web3cli.exceptions import Web3CliError
from web3core.exceptions import AbiOverflow, NotSupportedYet
from web3core.helpers.abi import (
    decode_function_data,
    get_event_full_signatures,
    get_event_names,
    get_event_signatures,
    get_function_full_signatures,
    get_function_names,
    get_function_signatures,
    parse_abi_value,
)


def test_get_function_names(erc20_abi: ABI) -> None:
    assert sorted(get_function_names(erc20_abi)) == sorted(
        [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ]
    )


def test_get_function_signatures(erc20_abi: ABI) -> None:
    assert sorted(get_function_signatures(erc20_abi)) == sorted(
        [
            "allowance(address,address)",
            "approve(address,uint256)",
            "balanceOf(address)",
            "decimals()",
            "name()",
            "symbol()",
            "totalSupply()",
            "transfer(address,uint256)",
            "transferFrom(address,address,uint256)",
        ]
    )


def test_get_function_full_signatures(erc20_abi: ABI) -> None:
    assert sorted(get_function_full_signatures(erc20_abi)) == sorted(
        [
            "allowance(address _owner, address _spender)",
            "approve(address _spender, uint256 _value)",
            "balanceOf(address _owner)",
            "decimals()",
            "name()",
            "symbol()",
            "totalSupply()",
            "transfer(address _to, uint256 _value)",
            "transferFrom(address _from, address _to, uint256 _value)",
        ]
    )


def test_get_event_names(erc20_abi: ABI) -> None:
    assert sorted(get_event_names(erc20_abi)) == sorted(
        [
            "Approval",
            "Transfer",
        ]
    )


def test_get_event_signatures(erc20_abi: ABI) -> None:
    assert sorted(get_event_signatures(erc20_abi)) == sorted(
        [
            "Approval(address,address,uint256)",
            "Transfer(address,address,uint256)",
        ]
    )


def test_get_event_full_signatures(erc20_abi: ABI) -> None:
    assert sorted(get_event_full_signatures(erc20_abi)) == sorted(
        [
            "Approval(address owner, address spender, uint256 value)",
            "Transfer(address from, address to, uint256 value)",
        ]
    )


def test_parse_abi_value_int() -> None:
    # Test parsing of signed and unsigned values
    assert parse_abi_value("0", "uint256") == 0
    assert parse_abi_value("0", "int256") == 0
    assert parse_abi_value("123", "uint256") == 123
    assert parse_abi_value("123", "int256") == 123
    assert parse_abi_value("0000123", "uint256") == 123
    assert parse_abi_value("0000123", "int256") == 123
    assert parse_abi_value("-123", "int256") == -123
    assert parse_abi_value("-0123", "int256") == -123
    assert parse_abi_value("123456789", "uint256") == 123456789
    assert parse_abi_value("123456789", "int256") == 123456789
    assert parse_abi_value("-123456789", "int256") == -123456789
    assert (
        parse_abi_value("123456789012345678901234567890", "uint256")
        == 123456789012345678901234567890
    )
    assert (
        parse_abi_value("123456789012345678901234567890", "int256")
        == 123456789012345678901234567890
    )
    # Test overflow of unsigned values
    assert parse_abi_value(str(2**255), "uint256") == 2**255
    assert pytest.raises(AbiOverflow, parse_abi_value, str(2**256), "uint256")
    assert pytest.raises(AbiOverflow, parse_abi_value, str(2**256), "uint256")
    # Test overflow of signed values
    assert parse_abi_value(str(2**254), "int256") == 2**254
    assert pytest.raises(AbiOverflow, parse_abi_value, str(2**255), "int256")
    # Can't parse negative values for unsigned values
    assert pytest.raises(ValueError, parse_abi_value, "-123", "uint256")
    assert pytest.raises(ValueError, parse_abi_value, "-123456789", "uint256")
    # Test strings in exponential notation
    assert parse_abi_value("1e+18", "uint256") == 10**18
    assert parse_abi_value("1e18", "uint256") == 10**18
    assert parse_abi_value("1.1e18", "uint256") == 11 * 10**17
    assert parse_abi_value("5e18", "uint256") == 5 * 10**18
    assert parse_abi_value("-5e18", "int256") == -5 * 10**18
    with pytest.raises(ValueError):
        assert parse_abi_value("-5e18", "uint256") == -5 * 10**18
    with pytest.raises(AbiOverflow):
        parse_abi_value("1e200", "uint256")
    with pytest.raises(ValueError):
        parse_abi_value("1e+18", "uint256", allow_exp_notation=False)
    with pytest.raises(ValueError):
        parse_abi_value("1e18", "uint256", allow_exp_notation=False)
    # Test that passing float numbers will error
    assert pytest.raises(ValueError, parse_abi_value, "1.1", "uint256")
    assert pytest.raises(ValueError, parse_abi_value, "1.12345e1", "uint256")
    assert pytest.raises(ValueError, parse_abi_value, "1.12345e2", "uint256")
    assert pytest.raises(ValueError, parse_abi_value, "1.12345e3", "uint256")
    assert pytest.raises(ValueError, parse_abi_value, "1.12345e4", "uint256")
    assert parse_abi_value("1.12345e5", "uint256") == 112345


def test_parse_abi_value_bool() -> None:
    assert parse_abi_value("0", "bool") is False
    assert parse_abi_value("1", "bool") is True
    assert parse_abi_value("false", "bool") is False
    assert parse_abi_value("true", "bool") is True
    assert parse_abi_value("False", "bool") is False
    assert parse_abi_value("True", "bool") is True
    assert parse_abi_value("FALSE", "bool") is False
    assert parse_abi_value("TRUE", "bool") is True
    assert parse_abi_value("False ", "bool") is False
    assert parse_abi_value(" True", "bool") is True
    assert parse_abi_value(" FALSE", "bool") is False
    assert parse_abi_value("TRUE ", "bool") is True
    assert parse_abi_value(" False ", "bool") is False
    assert parse_abi_value(" True ", "bool") is True
    assert parse_abi_value(" FALSE ", "bool") is False
    assert parse_abi_value("TRUE ", "bool") is True
    assert pytest.raises(ValueError, parse_abi_value, "2", "bool")
    assert pytest.raises(ValueError, parse_abi_value, "3", "bool")


def test_parse_abi_value_address() -> None:
    assert parse_abi_value("0x0000000000000000000000000000000000000000", "address") == (
        "0x0000000000000000000000000000000000000000"
    )
    assert parse_abi_value("0xdac17f958d2ee523a2206206994597c13d831ec7", "address") == (
        "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )
    assert pytest.raises(ValueError, parse_abi_value, "0x0000000", "address")
    assert pytest.raises(
        InvalidAddress,
        parse_abi_value,
        "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "address",
        checksum_addresses=False,
    )


def test_parse_abi_value_with_resolve_fn() -> None:
    def resolve_fn(name: str) -> str:
        if name == "alice":
            return "0x0000000000000000000000000000000000000001"
        elif name == "bob":
            return "0x0000000000000000000000000000000000000002"
        return name

    assert parse_abi_value("alice", "address", resolve_address_fn=resolve_fn) == (
        "0x0000000000000000000000000000000000000001"
    )

    assert parse_abi_value("bob", "address", resolve_address_fn=resolve_fn) == (
        "0x0000000000000000000000000000000000000002"
    )

    assert parse_abi_value("alice,bob", "address[]", resolve_address_fn=resolve_fn) == (
        [
            "0x0000000000000000000000000000000000000001",
            "0x0000000000000000000000000000000000000002",
        ]
    )

    assert parse_abi_value(
        "0x0000000000000000000000000000000000000003",
        "address",
        resolve_address_fn=resolve_fn,
    ) == ("0x0000000000000000000000000000000000000003")


def test_parse_abi_value_array_csv() -> None:
    assert parse_abi_value("True,False,true,false,1,0", "bool[]") == [
        True,
        False,
        True,
        False,
        True,
        False,
    ]
    assert parse_abi_value("123", "int256[]") == [123]
    assert parse_abi_value("-2,-1,0,1,2", "int256[]") == [-2, -1, 0, 1, 2]
    assert parse_abi_value("0,1,2,3,4", "uint256[]") == [0, 1, 2, 3, 4]
    assert parse_abi_value("0,1,2,3,4", "string[]") == ["0", "1", "2", "3", "4"]
    assert parse_abi_value("hello,world", "string[]") == ["hello", "world"]
    assert parse_abi_value('hello,"w,o,r,l,d"', "string[]") == ["hello", "w,o,r,l,d"]
    with pytest.raises(NotSupportedYet):
        parse_abi_value("whatever", "string[][]")


def test_parse_abi_value_tuple_csv() -> None:
    abi = cast(
        ABIFunctionParams,
        {
            "name": "TestTuple",
            "type": "tuple",
            "components": [
                {"name": "TestBool", "type": "bool"},
                {"name": "TestInt", "type": "int256"},
                {"name": "TestUint", "type": "uint256"},
                {"name": "TestString", "type": "string"},
                {"name": "TestAddress", "type": "address"},
            ],
        },
    )
    assert parse_abi_value(
        "True,-123,123,hello,0xdAC17F958D2ee523a2206206994597C13D831ec7",
        abi_input=abi,
    ) == {
        "TestBool": True,
        "TestInt": -123,
        "TestUint": 123,
        "TestString": "hello",
        "TestAddress": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    }
    with pytest.raises(ValueError):
        parse_abi_value("whatever", abi_type="tuple")
    with pytest.raises(
        Web3CliError, match="Provided 4 values for tuple argument TestTuple, expected 5"
    ):
        assert parse_abi_value("True,-123,123,hello", abi_input=abi)
    with pytest.raises(NotSupportedYet, match="Tuple of arrays not supported"):
        nested_abi = cast(
            ABIFunctionParams,
            {
                "name": "TestTuple",
                "type": "tuple",
                "components": [{"name": "TestSubArray", "type": "string[]"}],
            },
        )
        parse_abi_value("whatever", abi_input=nested_abi)
    with pytest.raises(NotSupportedYet, match="Tuple of tuples not supported"):
        nested_abi = cast(
            ABIFunctionParams,
            {
                "name": "TestTuple",
                "type": "tuple",
                "components": [{"name": "TestSubTuple", "type": "tuple"}],
            },
        )
        parse_abi_value("whatever", abi_input=nested_abi)


def test_parse_abi_value_string() -> None:
    assert parse_abi_value("hello", "string") == "hello"
    assert parse_abi_value("hello world", "string") == "hello world"
    assert (
        parse_abi_value("0xdAC17F958D2ee523a2206206994597C13D831ec7", "string")
        == "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )
    assert parse_abi_value("3", "string") == "3"
    assert parse_abi_value("False", "string") == "False"


def test_parse_abi_value_bytes() -> None:
    assert parse_abi_value("0", "bytes") == HexBytes("0")
    assert parse_abi_value("123", "bytes") == HexBytes("123")
    assert pytest.raises(Web3CliError, parse_abi_value, "q", "bytes")


def test_decode_function_data(erc20_abi: ABI) -> None:
    # transferFrom transaction on USDC contract (https://etherscan.io/tx/0x3f024aeca5e02128c5453d6f028b33fb43e061eb7ad584a8e090a9790f9b8d64)
    selector = "0x23b872dd"
    function_name = "transferFrom"
    signature = "transferFrom(address,address,uint256)"
    data_without_selector = "0000000000000000000000001c4d7f0c4df4c48d8628dcb913f2cb6b81bc0abb000000000000000000000000f16e9b0d03470827a95cdfd0cb8a8a3b46969b9100000000000000000000000000000000000000000000000000000000b2d05e00"
    data = selector + data_without_selector
    expected_parameters = {
        "_from": "0x1c4d7f0c4df4C48d8628DCB913F2Cb6B81Bc0Abb",
        "_to": "0xf16E9B0D03470827A95CDfd0Cb8a8A3b46969B91",
        "_value": 3000000000,
    }
    assert decode_function_data(erc20_abi, data)[0] == expected_parameters
    assert (
        decode_function_data(erc20_abi, data_without_selector, function_name)[0]
        == expected_parameters
    )
    assert (
        decode_function_data(erc20_abi, data_without_selector, function_name)[1]
        == signature
    )
