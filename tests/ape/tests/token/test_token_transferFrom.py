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
    print("accounts")
    print(accounts)
    sender_balance = TST.balanceOf(accounts[0])
    amount = sender_balance // 4

    TST.approve(accounts[1], amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert TST.balanceOf(accounts[0]) == sender_balance - amount


@pytest.mark.local
@pytest.mark.contracts
def test_receiver_balance_increases(accounts, TST):
    receiver_balance = TST.balanceOf(accounts[2])
    amount = TST.balanceOf(accounts[0]) // 4

    TST.approve(accounts[1], amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert TST.balanceOf(accounts[2]) == receiver_balance + amount


@pytest.mark.local
@pytest.mark.contracts
def test_caller_balance_not_affected(accounts, TST):
    caller_balance = TST.balanceOf(accounts[1])
    amount = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert TST.balanceOf(accounts[1]) == caller_balance


@pytest.mark.local
@pytest.mark.contracts
def test_caller_approval_affected(accounts, TST):
    approval_amount = TST.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    TST.approve(accounts[1], approval_amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], transfer_amount, sender=accounts[1])

    assert TST.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


@pytest.mark.local
@pytest.mark.contracts
def test_receiver_approval_not_affected(accounts, TST):
    approval_amount = TST.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    TST.approve(accounts[1], approval_amount, sender=accounts[0])
    TST.approve(accounts[2], approval_amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], transfer_amount, sender=accounts[1])

    assert TST.allowance(accounts[0], accounts[2]) == approval_amount


@pytest.mark.local
@pytest.mark.contracts
def test_total_supply_not_affected(accounts, TST):
    total_supply = TST.totalSupply()
    amount = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert TST.totalSupply() == total_supply


@pytest.mark.local
@pytest.mark.contracts
def test_returns_true(accounts, TST):
    amount = TST.balanceOf(accounts[0])
    TST.approve(accounts[1], amount, sender=accounts[0])
    tx = TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert tx.return_value is True


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_full_balance(accounts, TST):
    amount = TST.balanceOf(accounts[0])
    receiver_balance = TST.balanceOf(accounts[2])

    TST.approve(accounts[1], amount, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert TST.balanceOf(accounts[0]) == 0
    assert TST.balanceOf(accounts[2]) == receiver_balance + amount


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_zero_tokens(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    receiver_balance = TST.balanceOf(accounts[2])

    TST.approve(accounts[1], sender_balance, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[2], 0, sender=accounts[1])

    assert TST.balanceOf(accounts[0]) == sender_balance
    assert TST.balanceOf(accounts[2]) == receiver_balance


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_zero_tokens_without_approval(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    receiver_balance = TST.balanceOf(accounts[2])

    TST.transferFrom(accounts[0], accounts[2], 0, sender=accounts[1])

    assert TST.balanceOf(accounts[0]) == sender_balance
    assert TST.balanceOf(accounts[2]) == receiver_balance


@pytest.mark.local
@pytest.mark.contracts
def test_insufficient_balance(accounts, TST):
    balance = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], balance + 1, sender=accounts[0])
    with ape.reverts():
        TST.transferFrom(accounts[0], accounts[2], balance + 1, sender=accounts[1])


@pytest.mark.local
@pytest.mark.contracts
def test_insufficient_approval(accounts, TST):
    balance = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], balance - 1, sender=accounts[0])
    with ape.reverts():
        TST.transferFrom(accounts[0], accounts[2], balance, sender=accounts[1])


@pytest.mark.local
@pytest.mark.contracts
def test_no_approval(accounts, TST):
    balance = TST.balanceOf(accounts[0])

    with ape.reverts():
        TST.transferFrom(accounts[0], accounts[2], balance, sender=accounts[1])


@pytest.mark.local
@pytest.mark.contracts
def test_revoked_approval(accounts, TST):
    balance = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], balance, sender=accounts[0])
    TST.approve(accounts[1], 0, sender=accounts[0])

    with ape.reverts():
        TST.transferFrom(accounts[0], accounts[2], balance, sender=accounts[1])


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_to_self(accounts, TST):
    sender_balance = TST.balanceOf(accounts[0])
    amount = sender_balance // 4

    TST.approve(accounts[0], sender_balance, sender=accounts[0])
    TST.transferFrom(accounts[0], accounts[0], amount, sender=accounts[0])

    assert TST.balanceOf(accounts[0]) == sender_balance
    assert TST.allowance(accounts[0], accounts[0]) == sender_balance - amount


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_to_self_no_approval(accounts, TST):
    amount = TST.balanceOf(accounts[0])

    with ape.reverts():
        TST.transferFrom(accounts[0], accounts[0], amount, sender=accounts[0])


@pytest.mark.local
@pytest.mark.contracts
def test_transfer_event_fires(accounts, TST):
    amount = TST.balanceOf(accounts[0])

    TST.approve(accounts[1], amount, sender=accounts[0])
    tx = TST.transferFrom(accounts[0], accounts[2], amount, sender=accounts[1])

    assert len(tx.events) == 1
    assert tx.events[0].get("from") == accounts[0]
    assert tx.events[0].to == accounts[2]
    assert tx.events[0].value == amount
