"""Helper functions to send native coins and ERC20 tokens
to an arbitrary address"""

from cement import App
from eth_typing.encoding import HexStr
from web3cli.core.models.address import Address
from web3cli.core.models.chain import Chain
from web3cli.helpers.client_factory import make_wallet
from web3cli.core.exceptions import Web3CliError
from web3 import Web3
from web3cli.helpers.misc import get_coin


def send_coin_or_token(
    app: App,
    ticker: str,
    to: str,
    amount: float,
    unit: str = "ether",
) -> HexStr:
    """Send a native coin or transfer an ERC20 token to the given address.
    The function will automatically determine which coin or token to transfer
    based on the `ticker` argument. The recipient address can be either an
    actual hex address or an address tag."""
    tx_hash = None
    supported_native_coins = [c.coin.lower() for c in Chain.get_all()]
    if ticker.lower() in supported_native_coins:
        if ticker.lower() == get_coin(app).lower():
            tx_hash = send_native_coin(app, to, amount, unit)
        else:
            raise Web3CliError(
                f"Please change chain: on {app.chain} chain you can only send {get_coin(app)}"
            )
    else:
        tx_hash = send_erc20_token(app, ticker, to, amount, unit)
    return tx_hash


def send_native_coin(
    app: App,
    to: str,
    amount: float,
    unit: str = "ether",
) -> HexStr:
    """Send a native coin to the given address. The recipient address can be
    either an actual hex address or an address tag."""
    to_address = Address.resolve_address(to)
    tx_hash = make_wallet(app).sendEthInWei(
        to=to_address,
        valueInWei=Web3.toWei(amount, unit),
        maxPriorityFeePerGasInGwei=app.priority_fee,
    )
    return tx_hash


def send_erc20_token(
    app: App,
    ticker: str,
    to: str,
    amount: float,
    unit: str = "ether",
) -> HexStr:
    """Send an ERC20 token to the given address. The recipient address can be
    either an actual hex address or an address tag."""
    raise NotImplementedError(f"Ticker {ticker} not supported yet")
