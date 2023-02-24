import pytest
from web3.exceptions import InvalidAddress
from web3.types import ABI

from web3core.exceptions import AbiOverflow
from web3core.helpers.abi import (
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
    assert parse_abi_value("uint256", "0") == 0
    assert parse_abi_value("int256", "0") == 0
    assert parse_abi_value("uint256", "123") == 123
    assert parse_abi_value("int256", "123") == 123
    assert parse_abi_value("uint256", "0000123") == 123
    assert parse_abi_value("int256", "0000123") == 123
    assert parse_abi_value("int256", "-123") == -123
    assert parse_abi_value("int256", "-0123") == -123
    assert parse_abi_value("uint256", "123456789") == 123456789
    assert parse_abi_value("int256", "123456789") == 123456789
    assert parse_abi_value("int256", "-123456789") == -123456789
    assert (
        parse_abi_value("uint256", "123456789012345678901234567890")
        == 123456789012345678901234567890
    )
    assert (
        parse_abi_value("int256", "123456789012345678901234567890")
        == 123456789012345678901234567890
    )
    # Test overflow of unsigned values
    assert parse_abi_value("uint256", str(2**255)) == 2**255
    assert pytest.raises(AbiOverflow, parse_abi_value, "uint256", str(2**256))
    assert pytest.raises(AbiOverflow, parse_abi_value, "uint256", str(2**256))
    # Test overflow of signed values
    assert parse_abi_value("int256", str(2**254)) == 2**254
    assert pytest.raises(AbiOverflow, parse_abi_value, "int256", str(2**255))
    # Can't parse negative values for unsigned values
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "-123")
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "-123456789")
    # Test strings in exponential notation
    assert parse_abi_value("uint256", "1e+18") == 10**18
    assert parse_abi_value("uint256", "1e18") == 10**18
    assert parse_abi_value("uint256", "1.1e18") == 11 * 10**17
    assert parse_abi_value("uint256", "5e18") == 5 * 10**18
    assert parse_abi_value("int256", "-5e18") == -5 * 10**18
    with pytest.raises(ValueError):
        assert parse_abi_value("uint256", "-5e18") == -5 * 10**18
    with pytest.raises(AbiOverflow):
        parse_abi_value("uint256", "1e200")
    with pytest.raises(ValueError):
        parse_abi_value("uint256", "1e+18", allow_exp_notation=False)
    with pytest.raises(ValueError):
        parse_abi_value("uint256", "1e18", allow_exp_notation=False)
    # Test that passing float numbers will error
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "1.1")
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "1.12345e1")
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "1.12345e2")
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "1.12345e3")
    assert pytest.raises(ValueError, parse_abi_value, "uint256", "1.12345e4")
    assert parse_abi_value("uint256", "1.12345e5") == 112345


def test_parse_abi_value_bool() -> None:
    assert parse_abi_value("bool", "0") is False
    assert parse_abi_value("bool", "1") is True
    assert parse_abi_value("bool", "false") is False
    assert parse_abi_value("bool", "true") is True
    assert parse_abi_value("bool", "False") is False
    assert parse_abi_value("bool", "True") is True
    assert parse_abi_value("bool", "FALSE") is False
    assert parse_abi_value("bool", "TRUE") is True
    assert parse_abi_value("bool", "False ") is False
    assert parse_abi_value("bool", " True") is True
    assert parse_abi_value("bool", " FALSE") is False
    assert parse_abi_value("bool", "TRUE ") is True
    assert parse_abi_value("bool", " False ") is False
    assert parse_abi_value("bool", " True ") is True
    assert parse_abi_value("bool", " FALSE ") is False
    assert parse_abi_value("bool", "TRUE ") is True
    assert pytest.raises(ValueError, parse_abi_value, "bool", "2")
    assert pytest.raises(ValueError, parse_abi_value, "bool", "3")


def test_parse_abi_value_address() -> None:
    assert parse_abi_value("address", "0x0000000000000000000000000000000000000000") == (
        "0x0000000000000000000000000000000000000000"
    )
    assert parse_abi_value("address", "0xdac17f958d2ee523a2206206994597c13d831ec7") == (
        "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )
    assert pytest.raises(ValueError, parse_abi_value, "address", "0x0000000")
    assert pytest.raises(
        InvalidAddress,
        parse_abi_value,
        "address",
        "0xdac17f958d2ee523a2206206994597c13d831ec7",
        checksum_addresses=False,
    )


def test_parse_abi_value_with_resolve_fn() -> None:
    def resolve_fn(name: str) -> str:
        if name == "alice":
            return "0x0000000000000000000000000000000000000001"
        elif name == "bob":
            return "0x0000000000000000000000000000000000000002"
        return name

    assert parse_abi_value("address", "alice", resolve_address_fn=resolve_fn) == (
        "0x0000000000000000000000000000000000000001"
    )

    assert parse_abi_value("address", "bob", resolve_address_fn=resolve_fn) == (
        "0x0000000000000000000000000000000000000002"
    )

    assert parse_abi_value("address[]", "alice,bob", resolve_address_fn=resolve_fn) == (
        [
            "0x0000000000000000000000000000000000000001",
            "0x0000000000000000000000000000000000000002",
        ]
    )

    assert parse_abi_value(
        "address",
        "0x0000000000000000000000000000000000000003",
        resolve_address_fn=resolve_fn,
    ) == ("0x0000000000000000000000000000000000000003")


def test_parse_abi_value_array_csv() -> None:
    assert parse_abi_value("bool[]", "True,False,true,false,1,0") == [
        True,
        False,
        True,
        False,
        True,
        False,
    ]
    assert parse_abi_value("int256[]", "-2,-1,0,1,2") == [-2, -1, 0, 1, 2]
    assert parse_abi_value("uint256[]", "0,1,2,3,4") == [0, 1, 2, 3, 4]
    assert parse_abi_value("string[]", "0,1,2,3,4") == ["0", "1", "2", "3", "4"]
    assert parse_abi_value("string[]", "hello,world") == ["hello", "world"]
    assert parse_abi_value("string[]", 'hello,"w,o,r,l,d"') == ["hello", "w,o,r,l,d"]


def test_parse_abi_value_string() -> None:
    assert parse_abi_value("string", "hello") == "hello"
    assert parse_abi_value("string", "hello world") == "hello world"
    assert (
        parse_abi_value("string", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
        == "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )
    assert parse_abi_value("string", "3") == "3"
    assert parse_abi_value("string", "False") == "False"
