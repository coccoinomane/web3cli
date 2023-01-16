from web3.types import ABI

from web3core.helpers.abi import (
    get_event_full_signatures,
    get_event_names,
    get_event_signatures,
    get_function_full_signatures,
    get_function_names,
    get_function_signatures,
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
