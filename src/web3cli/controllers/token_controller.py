import decimal

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.render import render_web3py
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address


class TokenController(Controller):
    """Handler of the `w3 token` command"""

    class Meta:
        label = "token"
        help = "transfer and approve tokens"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Approve the given spender to spend the given amount of tokens",
        arguments=[
            (["token"], {"help": "Token to approve"}),
            (["spender"], {"help": "Address or name of the spender to be approved"}),
            (
                ["amount"],
                {
                    "help": "Amount of tokens to approve, in wei. Leave empty to approve the maximum amount",
                    "type": int,
                    "nargs": "?",
                },
            ),
            (
                ["--check"],
                {
                    "help": "Do not approve if the spender already has enough allowance",
                    "action": "store_true",
                },
            ),
            args.tx_return(),
            args.tx_dry_run(),
            args.tx_call(),
            args.tx_gas_limit(),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            args.force(),
        ],
    )
    def approve(self) -> None:
        # Parse arguments
        spender = resolve_address(self.app.pargs.spender, chain=self.app.chain.name)
        # Initialize client
        client = make_contract_wallet(self.app, self.app.pargs.token)
        # Compute amount in
        if not self.app.pargs.amount:
            amount = 2**256 - 1
        else:
            amount_token_units = decimal.Decimal(self.app.pargs.amount)
            decimals = client.functions["decimals"]().call()
            amount = int(amount_token_units * 10**decimals)
        # Confirm
        if not self.app.pargs.force:
            what = (
                (str(self.app.pargs.amount) if self.app.pargs.amount else "infinite")
                + " "
                + self.app.pargs.token
            )
            print(
                f"You are about to approve {self.app.pargs.spender} on chain {self.app.chain.name} to spend {what} in your name"
            )
            yes_or_exit(logger=self.app.log.info)
        # Approve
        if self.app.pargs.check:
            self.app.log.debug("Checking token allowance...")
            allowance = client.functions["allowance"](
                self.app.signer.address, spender
            ).call()
            # If allowance is not sufficient, approve
            if allowance >= amount:
                self.app.log.info(
                    "Not approving: token allowance is already sufficient"
                )
                return
        self.app.log.debug("Approving DEX spender spend token...")
        output = send_contract_tx(
            self.app,
            client,
            client.functions["approve"](spender, amount),
        )
        # Print output
        render_web3py(self.app, output)
