from pprint import pformat

from cement import ex

from web3cli.controllers.controller import Controller
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
        help="Sign the given message and show the signed message, as returned by web3.py",
        arguments=[(["msg"], {"action": "store"})],
    )
    def sign(self) -> None:
        signer_ready_or_raise(self.app)
        signed_message = make_wallet(self.app).signMessage(self.app.pargs.msg)
        self.app.print(pformat(signed_message._asdict()))
