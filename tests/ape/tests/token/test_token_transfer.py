# mypy: ignore-errors
# from https://github.com/brownie-mix/token-mix

import pytest

import ape

# @pytest.fixture(scope="function", autouse=True)
# def isolate(fn_isolation):
#     pass


@pytest.mark.local
@pytest.mark.contracts
def test_sender_balance_decreases(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    amount = sender_balance // 4

    TST.transfer(accounts[1], amount, sender=accounts[0])

    assert TST.balanceOf(accounts[0]) == sender_balance - amount


@pytest.mark.local
@pytest.mark.contracts
def test_receiver_balance_increases(accounts, TST):
    receiver_balance = TST.balanceOf(accounts[1])
    amount = TST.balanceOf(accounts[0]) // 4

    TST.transfer(accounts[1], amount, sender=accounts[0])

    assert TST.balanceOf(accounts[1]) == receiver_balance + amount


@pytest.mark.local
@pytest.mark.contracts
def test_total_supply_not_affected(accounts, TST):
    total_supply = TST.totalSupply()
    amount = TST.balanceOf(accounts[0])

    TST.transfer(accounts[1], amount, sender=accounts[0])

    assert TST.totalSupply() == total_supply


@pytest.mark.local
@pytest.mark.contracts
def test_returns_true(accounts, TST):
    amount = TST.balanceOf(accounts[0])
    tx = TST.transfer(accounts[1], amount, sender=accounts[0])

    assert tx.return_value is True


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_full_balance(accounts, TST):
    amount = TST.balanceOf(accounts[0])
    receiver_balance = TST.balanceOf(accounts[1])

    TST.transfer(accounts[1], amount, sender=accounts[0])

    assert TST.balanceOf(accounts[0]) == 0
    assert TST.balanceOf(accounts[1]) == receiver_balance + amount


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_zero_tokens(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    receiver_balance = TST.balanceOf(accounts[1])

    TST.transfer(accounts[1], 0, sender=accounts[0])

    assert TST.balanceOf(accounts[0]) == sender_balance
    assert TST.balanceOf(accounts[1]) == receiver_balance


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_to_self(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    amount = sender_balance // 4

    TST.transfer(accounts[0], amount, sender=accounts[0])

    assert TST.balanceOf(accounts[0]) == sender_balance


@pytest.mark.local
@pytest.mark.contracts
def test_insufficient_balance(accounts, TST):
    balance = TST.balanceOf(accounts[0])

    with ape.reverts():
        TST.transfer(accounts[1], balance + 1, sender=accounts[0])


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_event_fires(accounts, TST):
    amount = TST.balanceOf(accounts[0])
    tx = TST.transfer(accounts[1], amount, sender=accounts[0])

    assert len(tx.events) == 1
    assert tx.events[0].get("from") == accounts[0]
    assert tx.events[0].to == accounts[1]
    assert tx.events[0].value == amount
