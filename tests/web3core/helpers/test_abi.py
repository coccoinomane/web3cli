import pytest
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
