# mypy: ignore-errors
# from https://github.com/brownie-mix/TST-mix

import pytest

# @pytest.fixture(scope="function", autouse=True)
# def isolate(fn_isolation):
#     pass


@pytest.mark.local
@pytest.mark.contracts
@pytest.mark.parametrize("idx", range(5))
def test_initial_approval_is_zero(TST, accounts, idx):
    assert TST.allowance(accounts[0], accounts[idx]) == 0


@pytest.mark.local
@pytest.mark.contracts
def test_approve(TST, accounts):
    TST.approve(accounts[1], 10**19, sender=accounts[0])

    assert TST.allowance(accounts[0], accounts[1]) == 10**19


@pytest.mark.local
@pytest.mark.contracts
def test_modify_approve(TST, accounts):
    TST.approve(accounts[1], 10**19, sender=accounts[0])
    TST.approve(accounts[1], 12345678, sender=accounts[0])

    assert TST.allowance(accounts[0], accounts[1]) == 12345678


@pytest.mark.local
@pytest.mark.contracts
def test_revoke_approve(TST, accounts):
    TST.approve(accounts[1], 10**19, sender=accounts[0])
    TST.approve(accounts[1], 0, sender=accounts[0])

    assert TST.allowance(accounts[0], accounts[1]) == 0


@pytest.mark.local
@pytest.mark.contracts
def test_approve_self(TST, accounts):
    TST.approve(accounts[0], 10**19, sender=accounts[0])

    assert TST.allowance(accounts[0], accounts[0]) == 10**19


@pytest.mark.local
@pytest.mark.contracts
def test_only_affects_target(TST, accounts):
    TST.approve(accounts[1], 10**19, sender=accounts[0])

    assert TST.allowance(accounts[1], accounts[0]) == 0


@pytest.mark.local
@pytest.mark.contracts
def test_returns_true(TST, accounts):
    tx = TST.approve(accounts[1], 10**19, sender=accounts[0])

    assert tx.return_value is True


@pytest.mark.local
@pytest.mark.contracts
def test_approval_event_fires(accounts, TST):
    tx = TST.approve(accounts[1], 10**19, sender=accounts[0])

    assert len(tx.events) == 1
    assert tx.events[0].owner == accounts[0]
    assert tx.events[0].spender == accounts[1]
    assert tx.events[0].value == 10**19
