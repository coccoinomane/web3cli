import json
from pprint import pformat

from cement import ex
from web3 import Web3

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.args import parse_block
from web3cli.helpers.client_factory import make_client
from web3core.helpers.client_factory import make_base_wallet
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
            args.block(),
            (
                ["-u", "--unit"],
                {
                    "help": "optionally specify the unit to use to show the balance (wei, gwei, etc). If you need exact comparisons, use wei.",
                    "default": "ether",
                },
            ),
            *args.chain_and_rpc(),
        ],
    )
    def balance(self) -> None:
        address = resolve_address(self.app.pargs.address, chain=self.app.chain.name)
        balance = make_client(self.app).w3.eth.get_balance(
            Web3.to_checksum_address(address),
            block_identifier=parse_block(self.app, "block"),
        )
        if self.app.pargs.unit != "wei":
            balance = Web3.from_wei(balance, self.app.pargs.unit)
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
        arguments=[args.block("block_identifier", nargs="?"), *args.chain_and_rpc()],
    )
    def block(self) -> None:
        block_identifier = parse_block(self.app, "block_identifier")
        block = make_client(self.app).w3.eth.get_block(block_identifier)
        block_as_dict = json.loads(Web3.to_json(block))
        self.app.render(block_as_dict, indent=4, handler="json")

    @ex(
        help="Sign the given message and show the signed message, as returned by web3.py",
        arguments=[(["msg"], {"action": "store"}), args.signer()],
    )
    def sign(self) -> None:
        wallet = make_base_wallet(
            chain=None, signer=self.app.signer, password=self.app.app_key, node_uri=None
        )
        signed_message = wallet.sign_message(self.app.pargs.msg)
        self.app.print(pformat(signed_message._asdict()))

    @ex(
        help="Get the current gas price in gwei by calling the eth_gasPrice method. For EIP1559 chains, this should return the max priority fee per gas.",
        arguments=[*args.chain_and_rpc()],
    )
    def gas_price(self) -> None:
        gas_price_in_wei = make_client(self.app).w3.eth.gas_price
        gas_price_in_gwei = Web3.from_wei(gas_price_in_wei, "gwei")
        self.app.render(gas_price_in_gwei)

    @ex(
        help="Get the base fee in gwei of the last block. Will error for non-EIP1559 chains.",
        arguments=[*args.chain_and_rpc()],
    )
    def base_fee(self) -> None:
        try:
            base_fee_in_wei = make_client(self.app).w3.eth.get_block("latest")[
                "baseFeePerGas"
            ]
        except KeyError:
            raise Web3CliError(
                f"Could not find base fee. Please check that chain '{self.app.chain.name}' is EIP-1599 compatible."
            )
        base_fee_in_gwei = Web3.from_wei(base_fee_in_wei, "gwei")
        self.app.render(base_fee_in_gwei)
