from web3core.db import DB
from web3core.helpers.database import init_db
from web3core.helpers.seed import populate_db
from web3core.models import MODELS


def main(populate: bool = True) -> None:
    """Create a new in-memory database and populate it with sample data"""
    init_db(DB, MODELS, ":memory:")
    if populate:
        populate_db()
