import decimal
from time import time

import web3
from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers import args
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.render import render_web3py
from web3cli.helpers.signer import signer_ready_or_raise
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers import dex
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address
from web3core.models.address import Address
from web3core.models.contract import Contract
from web3core.models.signer import Signer


class SwapController(Controller):
    """Handler of the `w3 swap` command"""

    class Meta:
        label = "swap"
        help = "swap tokens using a DEX"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Swap tokens using a DEX",
        arguments=[
            (["dex"], args.swap_dex()),
            (["amount"], args.swap_amount()),
            (["token_in"], args.swap_token_in()),
            (["token_out"], args.swap_token_out()),
            (
                ["--slippage"],
                args.swap_slippage(help="Not implemented yet", default=None),
            ),
            (["--min-out"], args.swap_min_out()),
            (["--to"], args.swap_to()),
            (["--approve"], args.swap_approve()),
            (["--deadline"], args.swap_deadline()),
            (["--return"], args.tx_return()),
            (["--dry-run"], args.tx_dry_run()),
            (["--call"], args.tx_call()),
            (["--gas-limit"], args.tx_gas_limit()),
            (["-f", "--force"], args.force()),
        ],
    )
    def swap(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        signer = Signer.get_by_name(self.app.signer)
        # Parse arguments
        to = self.app.pargs.to if self.app.pargs.to else signer.address
        to_address = resolve_address(to, [Address, Signer])
        amount_in_token_units = decimal.Decimal(self.app.pargs.amount)
        token_in = resolve_address(
            self.app.pargs.token_in, [Contract], self.app.chain_name
        )
        token_out = resolve_address(
            self.app.pargs.token_out, [Contract], self.app.chain_name
        )
        # Check if the DEX is supported
        Contract.get_by_name_chain_and_type_or_raise(
            self.app.pargs.dex, self.app.chain_name, "uniswap_v2"
        )
        # Initialize clients
        router_client = make_contract_wallet(self.app, self.app.pargs.dex)
        token_in_client = make_contract_wallet(self.app, self.app.pargs.token_in)
        token_out_client = make_contract_wallet(self.app, self.app.pargs.token_out)
        # Compute amount in
        decimals_in = token_in_client.functions["decimals"]().call()
        amount_in = int(amount_in_token_units * 10**decimals_in)
        # Throw if the amount is larger than the balance
        balance = token_in_client.functions["balanceOf"](signer.address).call()
        if amount_in > balance:
            raise Web3CliError(
                f"Not enough {self.app.pargs.token_in} to swap. Balance: {balance/10**decimals_in}"
            )
        # Compute amount out
        decimals_out = token_out_client.functions["decimals"]().call()
        try:
            amounts_out = router_client.functions["getAmountsOut"](
                amount_in, [token_in, token_out]
            ).call()
        except web3.exceptions.ContractLogicError as e:
            raise Web3CliError(
                f"Could not compute the amount out. This is probably because the pair {self.app.pargs.token_in}-{self.app.pargs.token_out} is not supported by the DEX. Original error: {e}"
            )
        amount_out = amounts_out[1]
        amount_out_token_units = decimal.Decimal(amount_out) / 10**decimals_out
        # Compute minimum amount out
        min_amount_out = 0
        # - from min_out argument
        if self.app.pargs.min_out:
            min_amount_out_token_units = decimal.Decimal(self.app.pargs.min_out)
            min_amount_out = min(
                min_amount_out, int(min_amount_out_token_units * 10**decimals_out)
            )
            if amount_out < min_amount_out:
                raise Web3CliError(
                    f"Amount out is too low: {amount_out_token_units} < {min_amount_out_token_units}"
                )
        # - from slippage argument
        if self.app.pargs.slippage:
            # NOT IMPLEMENTED YET
            pass
        # Confirm transaction
        # TODO: move to send_contract_tx function
        if not self.app.pargs.force:
            print(f"You are about to perform the following swap:")
            what_in = f"{self.app.pargs.amount} {self.app.pargs.token_in}"
            what_out = f"{amount_out_token_units} {self.app.pargs.token_out}"
            print(f"  {what_in} -> {what_out}")
            if self.app.pargs.min_out:
                what_min_out = (
                    f"{min_amount_out_token_units} {self.app.pargs.token_out}"
                )
                print(f"  Minimum you will get: {what_min_out}")
            if self.app.pargs.slippage:
                print(f"  Max slippage: {self.app.pargs.slippage}%")
            if self.app.pargs.dry_run:
                print("  Dry run: yes")
            print(f"  Dex: {self.app.pargs.dex}")
            print(f"  Chain: {self.app.chain_name}")
            print(f"  From: {self.app.signer} ({signer.address})")
            if signer.address != to_address:
                print(f"  Final recipient: {to_address}")
            print(f"  Contract address: {router_client.contract_address}")
            print(f"  Token in address: {token_in}")
            print(f"  Token out address: {token_out}")
            yes_or_exit(logger=self.app.log.info)
        # Approve
        if self.app.pargs.approve:
            self.app.log.debug("Checking token allowance...")
            # Check allowance
            allowance = token_in_client.functions["allowance"](
                signer.address, router_client.contract_address
            ).call()
            # If allowance is not sufficient, approve
            if allowance < amount_in:
                approve_function = token_in_client.functions["approve"](
                    router_client.contract_address, amount_in
                )
                send_contract_tx(
                    self.app,
                    token_in_client,
                    approve_function,
                    fetch_data=False,
                    fetch_receipt=True,
                )
            else:
                self.app.log.debug("Token allowance is already sufficient")
        # Build swap function
        swap_function = dex.get_swap_function(
            router_client,
            amount_in,
            min_amount_out,
            token_in,
            token_out,
            to_address,
            int(time()) + self.app.pargs.deadline,
        )
        # Swap or simulate
        output = send_contract_tx(self.app, router_client, swap_function)
        # Print output
        render_web3py(self.app, output)
