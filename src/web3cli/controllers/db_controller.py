from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.database import delete_db_file, get_db_filepath
from web3cli.helpers.render import render
from web3core.helpers.misc import yes_or_exit


class DbController(Controller):
    """Base controller for the `w3 db` command"""

    class Meta:
        label = "db"
        help = "Interact with the local database of the app"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="delete the entire db: signers, addresses, chains, etc",
        arguments=[args.force()],
    )
    def delete(self) -> None:
        if not self.app.pargs.force:
            yes_or_exit(
                intro="WARNING: This will delete all stored info, such as signers, addresses, transactions and chains.\n",
                logger=self.app.log.info,
            )
        db_path = get_db_filepath(self.app)
        if db_path == ":memory:":
            self.app.log.info("Database is in-memory, nothing to delete")
            return
        if delete_db_file(self.app):
            self.app.log.info(f"Database file deleted ({db_path})")
        else:
            self.app.log.info(f"Database not found at {db_path}")

    @ex(help="show the path of the database file")
    def where(self) -> None:
        render(self.app, get_db_filepath(self.app))
