#!/usr/bin/python3

from brownie import Token, accounts


def main() -> None:
    return Token.deploy("Test Token", "TST", 18, 1e21, {"from": accounts[0]})
