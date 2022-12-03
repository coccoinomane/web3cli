from pprint import pformat
from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.input import yes_or_exit
from web3cli.core.models.address import Address
from web3cli.helpers.misc import get_coin
from web3cli.helpers.send import send_coin_or_token
from web3cli.helpers.version import get_version_message
from web3cli.helpers.client_factory import make_client, make_wallet
from web3cli.helpers import args


class DbBaseController(Controller):
    """Base controller for the `w3 db` command"""

    class Meta:
        label = "db"
        help = "Interact with the local database of web3cli"
        stacked_type = "nested"
        stacked_on = "base"
