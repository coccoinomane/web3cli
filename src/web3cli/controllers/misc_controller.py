import json
from pprint import pformat

from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.args import parse_block
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_client, make_wallet
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.helpers.resolve import resolve_address


class MiscController(Controller):
    """Handler of simple top-level commands"""

    class Meta:
        label = "misc"
        help = "simple top-level commands"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Get the balance of the given address in the blockchain coin (ETH, BNB, AVAX, etc)",
        arguments=[
            (["address"], {"action": "store"}),
            (
                ["unit"],
                {
                    "help": "optionally specify the unit to use to show the balance (wei, gwei, etc). If you need exact comparisons, use wei.",
                    "nargs": "?",
                    "default": "ether",
                },
            ),
        ],
    )
    def balance(self) -> None:
        chain_ready_or_raise(self.app)
        address = resolve_address(self.app.pargs.address, chain=self.app.chain_name)
        balance = make_client(self.app).w3.eth.get_balance(
            Web3.toChecksumAddress(address)
        )
        if self.app.pargs.unit != "wei":
            balance = Web3.fromWei(balance, self.app.pargs.unit)
        self.app.render(
            {
                "amount": balance,
                "ticker": self.app.chain.coin,
                "unit": self.app.pargs.unit,
            },
            "balance.jinja2",
            handler="jinja2",
        )

    @ex(
        help="Get the latest block, or the block corresponding to the given identifier",
        arguments=[(["block_identifier"], args.block())],
    )
    def block(self) -> None:
        chain_ready_or_raise(self.app)
        block_identifier = parse_block(self.app, "block_identifier")
        block = make_client(self.app).w3.eth.get_block(block_identifier)
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
