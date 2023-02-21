import decimal

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.render import render_web3py
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address
from web3core.helpers.tx import send_contract_transaction
from web3core.models.signer import Signer


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
            (["--return"], args.tx_return()),
            (["--dry-run"], args.tx_dry_run()),
            (["--call"], args.tx_call()),
            (["--gas-limit"], args.tx_gas_limit()),
            (["-f", "--force"], args.force()),
        ],
    )
    def approve(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        signer = Signer.get_by_name(self.app.signer)
        # Parse arguments
        spender = resolve_address(self.app.pargs.spender, chain=self.app.chain_name)
        dry_run, tx_return, tx_call = args.parse_tx_args(self.app)
        # Initialize client
        token_client = make_contract_wallet(self.app, self.app.pargs.token)
        # Compute amount in
        if not self.app.pargs.amount:
            amount = 2**256 - 1
        else:
            amount_token_units = decimal.Decimal(self.app.pargs.amount)
            decimals = token_client.functions["decimals"]().call()
            amount = int(amount_token_units * 10**decimals)
        # Confirm
        if not self.app.pargs.force:
            what = (
                (str(self.app.pargs.amount) if self.app.pargs.amount else "infinite")
                + " "
                + self.app.pargs.token
            )
            print(
                f"You are about to approve {self.app.pargs.spender} on chain {self.app.chain_name} to spend {what} in your name"
            )
            yes_or_exit(logger=self.app.log.info)
        # Approve
        if self.app.pargs.check:
            self.app.log.debug("Checking token allowance...")
            allowance = token_client.functions["allowance"](
                signer.address, spender
            ).call()
            # If allowance is not sufficient, approve
            if allowance >= amount:
                self.app.log.info(
                    "Not approving: token allowance is already sufficient"
                )
                return
        self.app.log.debug("Approving DEX spender spend token...")
        approve_function = token_client.functions["approve"](spender, amount)
        approve_tx_life = send_contract_transaction(
            token_client,
            approve_function,
            dry_run=dry_run,
            call=tx_call,
            fetch_data=True if tx_return in ["data", "all"] else False,
            fetch_receipt=True if tx_return in ["receipt", "all"] else False,
            maxPriorityFeePerGasInGwei=self.app.priority_fee,
        )
        # Wait for tx to be mined
        if not dry_run:
            approve_tx_hash = approve_tx_life["hash"]
            self.app.log.info(f"Approval tx: {approve_tx_hash}")
            token_client.getTransactionReceipt(approve_tx_hash)
            self.app.log.debug(f"Approval tx mined")
        else:
            self.app.log.info("Dry run: skipping approval")
        if tx_return == "all":
            render_web3py(self.app, approve_tx_life)
        else:
            render_web3py(self.app, approve_tx_life[tx_return])
