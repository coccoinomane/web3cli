import argparse
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
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address
from web3core.helpers.tx import send_contract_transaction
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
            (
                ["dex"],
                {
                    "help": "name of the DEX to use, e.g. uniswap_v2, pancakeswap_v2, traderjoe_v2, etc.",
                },
            ),
            (
                ["token_in"],
                {"help": "ticker of the coin to swap from, e.g. USDC"},
            ),
            (["amount"], {"help": "how much to swap"}),
            (
                ["token_out"],
                {"help": "ticker of the coin to swap to, e.g. USDT"},
            ),
            (
                ["--slippage"],
                {
                    "help": "max slippage percentage you are willing to tolerate. Defaults to 0.5%.",
                    "default": 0.5,
                    "type": float,
                },
            ),
            (
                ["--to"],
                {
                    "help": "optionally specify the address to receive the swapped tokens. Defaults to the signer's address.",
                },
            ),
            (
                ["--approve"],
                {
                    "help": "whether to approve the DEX to spend the token_in. Defaults to False.",
                    "action": argparse.BooleanOptionalAction,
                    "default": False,
                },
            ),
            (
                ["--deadline"],
                {
                    "help": "deadline for the swap, in seconds. Defaults to 15 minutes.",
                    "default": 15 * 60,
                    "type": int,
                },
            ),
            (["--return"], args.tx_return()),
            (["--dry-run"], args.tx_dry_run()),
            (["--call"], args.tx_call()),
            (["-f", "--force"], args.force()),
        ],
    )
    def swap(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        signer = Signer.get_by_name(self.app.signer)
        # Parse arguments
        dry_run, tx_return, tx_call = args.parse_tx_args(self.app)
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
        # Enforce slippage
        # if not dry_run:
        #     amount_out = amounts_out[1]
        #     amount_out_token_units = decimal.Decimal(amount_out) / 10**decimals_out
        #     slippage = (amount_out_token_units - amount_in_token_units) / amount_in_token_units
        #     if slippage > self.app.pargs.slippage / 100:
        #         raise Exception(f"Slippage is too high: {slippage * 100}%")
        # Confirm
        if not self.app.pargs.force and not dry_run:
            what_in = f"{amount_in_token_units} {self.app.pargs.token_in}"
            what_out = f"{amount_out_token_units} {self.app.pargs.token_out}"
            print(f"You are about to peform the following swap:")
            print(f"  {what_in} -> {what_out}")
            print(f"  Dex: {self.app.pargs.dex}")
            print(f"  Chain: {self.app.chain_name}")
            print(f"  From: {self.app.signer} ({signer.address})")
            if signer.address != to_address:
                print(f"  Final recipient: {to_address}")
            print(f"  Contract address: {router_client.contractAddress}")
            print(f"  Token in address: {token_in}")
            print(f"  Token out address: {token_out}")
            # print(f"  Slippage: {self.app.pargs.slippage}%")
            yes_or_exit(logger=self.app.log.info)
        # Approve
        if self.app.pargs.approve:
            self.app.log.debug("Checking token allowance...")
            # Check allowance
            allowance = token_in_client.functions["allowance"](
                signer.address, router_client.contractAddress
            ).call()
            # If allowance is not sufficient, approve
            if allowance < amount_in:
                self.app.log.info("Approving DEX to spend token_in...")
                approve_function = token_in_client.functions["approve"](
                    router_client.contractAddress, amount_in
                )
                approve_tx_life = send_contract_transaction(
                    token_in_client,
                    approve_function,
                    dry_run=dry_run,
                    call=tx_call,
                    fetch_receipt=True,
                    maxPriorityFeePerGasInGwei=self.app.priority_fee,
                )
                # Wait for tx to be mined
                if not dry_run:
                    approve_tx_hash = approve_tx_life["hash"]
                    self.app.log.info(f"Approval tx: {approve_tx_hash}")
                    token_in_client.getTransactionReceipt(approve_tx_hash)
                    self.app.log.debug(f"Approval tx mined")
            else:
                self.app.log.debug("Token allowance is already sufficient")
        # Build swap function
        swap_function = router_client.functions["swapExactTokensForTokens"](
            amount_in,
            0,
            [token_in, token_out],
            to_address,
            int(time()) + self.app.pargs.deadline,
        )
        # Inform user
        if not dry_run:
            self.app.log.debug("Swapping...")
        if dry_run and tx_call:
            self.app.log.debug("Simulating swap...")
        # Swap or simulate
        tx_life = send_contract_transaction(
            router_client,
            swap_function,
            dry_run=dry_run,
            call=tx_call,
            fetch_data=True if tx_return in ["data", "all"] else False,
            fetch_receipt=True if tx_return in ["receipt", "all"] else False,
            maxPriorityFeePerGasInGwei=self.app.priority_fee,
        )
        # Print output
        if tx_return == "all":
            render_web3py(self.app, tx_life)
        else:
            render_web3py(self.app, tx_life[tx_return])
