#!/usr/bin/python3

from ape import accounts, project


def main(name: str = "Test Token", symbol: str = "TST") -> None:
    project.Token.deploy(name, symbol, 18, 10**9 * 10**18, sender=accounts[0])
