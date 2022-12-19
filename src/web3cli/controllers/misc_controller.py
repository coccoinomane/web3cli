import json
from pprint import pformat

from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.core.helpers.web3 import format_attribute_dict
from web3cli.core.models.address import Address
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_client, make_wallet
from web3cli.helpers.signer import signer_ready_or_raise


class MiscController(Controller):
    """Handler of simple top-level commands"""

    class Meta:
        label = "misc"
        help = "simple top-level commands"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Get the balance of the given address in the blockchain coin (ETH, BNB, AVAX, etc)",
        arguments=[(["address"], {"action": "store"})],
    )
    def balance(self) -> None:
        chain_ready_or_raise(self.app)
        balance = make_client(self.app).getBalanceInEth(
            Address.resolve_address(self.app.pargs.address)
        )
        self.app.render(
            {"amount": balance, "ticker": self.app.chain.coin},
            "balance.jinja2",
            handler="jinja2",
        )

    @ex(
        help="Get the latest block, or the block corresponding to the given identifier",
        arguments=[
            (
                ["block_identifier"],
                {
                    "help": "Block identifier. Can be a block number, an hash, or one of the following: latest, earliest, pending, safe, finalized",
                    "nargs": "?",
                    "default": "latest",
                },
            )
        ],
    )
    def block(self) -> None:
        chain_ready_or_raise(self.app)
        block = None
        client = make_client(self.app)
        # In case a block number was given
        try:
            block = client.w3.eth.get_block(int(self.app.pargs.block_identifier))
        except ValueError:
            pass
        # In case a string
        if not block:
            block = client.w3.eth.get_block(self.app.pargs.block_identifier)
        block_as_dict = json.loads(Web3.toJSON(block))
        self.app.render(block_as_dict, indent=4, handler="json")

    @ex(
        help="Sign the given message and show the signed message, as returned by web3.py",
        arguments=[(["msg"], {"action": "store"})],
    )
    def sign(self) -> None:
        signer_ready_or_raise(self.app)
        signed_message = make_wallet(self.app).signMessage(self.app.pargs.msg)
        self.app.print(pformat(signed_message._asdict()))
