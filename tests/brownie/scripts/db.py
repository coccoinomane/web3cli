from brownie_tokens import ERC20

from brownie import accounts
from brownie.network.contract import Contract as BrownieContract
from web3core.db import DB
from web3core.helpers.database import init_db
from web3core.helpers.seed import populate_db
from web3core.models import MODELS


def main(populate: bool = True) -> None:
    """Create a new database and populate it with sample data"""
    init_db(DB, MODELS, ":memory:")
    if populate:
        populate_db()


def token() -> BrownieContract:
    """Mint an ERC20 token for testing with symbol TST and 18 decimals,
    and fund each account with 100 TST"""
    token = ERC20(name="Test Token", symbol="TST", decimals=18)
    for account in accounts:
        token._mint_for_testing(account.address, 100 * 10**6)
    return token
