from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers.database import delete_db_file, get_db_file
from web3core.helpers.misc import yes_or_exit


class DbBaseController(Controller):
    """Base controller for the `w3 db` command"""

    class Meta:
        label = "db"
        help = "Interact with the local database of web3cli"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="delete the entire db: signers, addresses, chains, etc",
        arguments=[
            (
                ["--force"],
                {
                    "help": "Delete without asking",
                    "action": "store_true",
                },
            ),
        ],
    )
    def delete(self) -> None:
        if not self.app.pargs.force:
            yes_or_exit(
                intro="WARNING: This will delete all stored info, such as signers, addresses, transactions and chains.\n",
                logger=self.app.log.info,
            )
        if delete_db_file(self.app):
            self.app.log.info(f"Database file deleted ({get_db_file(self.app)})")
        else:
            self.app.log.info(f"Database not found at {get_db_file(self.app)}")
