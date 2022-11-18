from typing import List
from brownie import accounts
import pytest
from web3cli.helpers.send import send_native_coin
from tests.main import Web3CliTest
from brownie.network.account import Account


# @pytest.mark.local
# def test_send_native_coin(accounts: List[Account]) -> None:
#     with Web3CliTest() as app:
#         app.run()
#         app.network
#         send_native_coin()
#     print(dir(accounts[0]))
