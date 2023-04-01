#!/usr/bin/python3

from brownie import Token, accounts


def main(name: str = "Test Token", symbol: str = "TST") -> None:
    return Token.deploy(name, symbol, 18, 1e9 * 1e18, {"from": accounts[0]})
