from web3core.helpers.database import init_db
from web3core.helpers.seed import populate_db


def main(populate: bool = True) -> None:
    """Create a new database and populate it with sample data"""
    init_db(":memory:")
    if populate:
        populate_db()
