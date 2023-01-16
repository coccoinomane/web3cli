"""Helper functions to send native coins and ERC20 tokens
to an arbitrary address"""

from decimal import Decimal
from typing import Union

from cement import App
from eth_typing.encoding import HexStr
from web3 import Web3

from web3cli.exceptions import Web3CliError
from web3cli.helpers.client_factory import make_erc20_wallet, make_wallet
from web3core.helpers.resolve import resolve_address
from web3core.models.address import Address
from web3core.models.chain import Chain
from web3core.models.contract import Contract
from web3core.models.signer import Signer


def send_coin_or_token(
    app: App,
    ticker: str,
    to: str,
    amount: Union[float, int],
    unit: str = None,
) -> HexStr:
    """Send a native coin or transfer an ERC20 token to the given address.

    The function will automatically determine which coin or token to transfer
    based on the `ticker` argument.

    For native coins, the unit can be any of the units supported by web3.py:
    wei, kwei, mwei, gwei, ether, etc. The default is ether, that is, a full
    unit of native coin.

    For ERC20 tokens, you have two options:
    1) leave the unit blank and specify the amount in token units, e.g. 3.4
        USDC or 14.2 UNI.
    2) set unit='smallest' and specify the amount as an integer, representing the
        the smallest possible subdivision of the token, determined by
        the token's decimals. See erc20_token_in_decimals for more details.
    """
    # Try to send native coin
    if ticker.lower() in [c.coin.lower() for c in Chain.get_all()]:
        if ticker.lower() != app.chain.coin.lower():
            raise Web3CliError(
                f"Please change chain: on {app.chain.name} chain you can only send {app.chain.coin}"
            )
        return send_native_coin(app, to, amount, unit)

    # Try to send token but first check if a contract exist with name=ticker
    token = Contract.get_by_name_and_chain(ticker, app.chain_name)
    if not token or not token.type == "erc20":
        raise Web3CliError(f"No ERC20 contract with name {ticker} on {app.chain.name}")
    return send_erc20_token(app, ticker, to, amount, unit)


def send_native_coin(
    app: App,
    to: str,
    amount: float,
    unit: str = None,
) -> HexStr:
    """Send a native coin to the given address"""
    return make_wallet(app).sendEthInWei(
        to=resolve_address(to, [Address, Signer]),
        valueInWei=Web3.toWei(amount, unit if unit else "ether"),
        maxPriorityFeePerGasInGwei=app.priority_fee,
    )


def send_erc20_token(
    app: App,
    ticker: str,
    to: str,
    amount: Union[float, int],
    unit: str = None,
) -> HexStr:
    """Send an ERC20 token to the given address either in token units (default)
    or using the smallest possible subdivision of the token (unit='smallest')."""
    if not unit:
        return send_erc20_token_in_token_units(app, ticker, to, amount)

    if unit == "smallest":
        if type(amount) != int:
            raise Web3CliError(
                "Please specify the amount as an integer when using unit='smallest'"
            )
        return send_erc20_token_in_decimals(app, ticker, to, amount)

    raise Web3CliError(
        f"Invalid unit {unit} for a token. Please use 'smallest' or leave blank"
    )


def send_erc20_token_in_decimals(
    app: App,
    ticker: str,
    to: str,
    amount: int = None,
) -> HexStr:
    """Send an ERC20 token to the given address, specifying the amount in the
    smallest subdivision of the token, which depends on the token's number of
    decimals.

    For example, if the token has 6 decimals, and you specify amount=1, the
    actual amount is 0.000001 in token units."""
    client = make_erc20_wallet(app, ticker)
    return client.transact(
        client.functions.transfer(resolve_address(to, [Address, Signer]), amount)
    )


def send_erc20_token_in_token_units(
    app: App,
    ticker: str,
    to: str,
    amount: float = None,
) -> HexStr:
    """Send an ERC20 token to the given address, specifying the amount in token
    units.

    This is a wrapper around `send_erc20_token` that automatically converts the
    amount to the smallest subdivision of the token, which depends on the
    token's decimals."""
    client = make_erc20_wallet(app, ticker)
    decimals = client.functions.decimals().call()
    amount = int(Decimal(amount) * 10**decimals)
    return send_erc20_token_in_decimals(app, ticker, to, amount)
