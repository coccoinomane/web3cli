import argparse
import decimal
from time import time

from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_client, make_contract_wallet
from web3cli.helpers.signer import signer_ready_or_raise
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
            (
                ["--dry-run"],
                {
                    "help": "whether to only simulate the swap, using eth_call. Will print the amounts that would have been swapped in a real run. Defaults to False.",
                    "action": argparse.BooleanOptionalAction,
                    "default": False,
                },
            ),
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
        # Initialize clients
        router_client = make_contract_wallet(self.app, self.app.pargs.dex)
        token_in_client = make_contract_wallet(self.app, self.app.pargs.token_in)
        token_out_client = make_contract_wallet(self.app, self.app.pargs.token_out)
        # Compute amount in
        decimals_in = token_in_client.functions["decimals"]().call()
        amount_in = int(amount_in_token_units * 10**decimals_in)
        # Compute amount out
        decimals_out = token_out_client.functions["decimals"]().call()
        amounts_out = router_client.functions["getAmountsOut"](
            amount_in, [token_in, token_out]
        ).call()
        amount_out = amounts_out[1]
        amount_out_token_units = decimal.Decimal(amount_out) / 10**decimals_out
        # Enforce slippage
        # if not self.app.pargs.dry_run:
        #     amount_out = amounts_out[1]
        #     amount_out_token_units = decimal.Decimal(amount_out) / 10**decimals_out
        #     slippage = (amount_out_token_units - amount_in_token_units) / amount_in_token_units
        #     if slippage > self.app.pargs.slippage / 100:
        #         raise Exception(f"Slippage is too high: {slippage * 100}%")
        # Confirm
        if not self.app.pargs.force:
            what_in = f"{amount_in_token_units} {self.app.pargs.token_in}"
            what_out = f"{amount_out_token_units} {self.app.pargs.token_out}"
            print(
                f"You are about to swap {what_in} ({token_in}) for {what_out} ({token_out}) on {self.app.chain.name} on {self.app.pargs.dex} ({router_client.contractAddress}) from wallet {self.app.signer} ({signer.address}) to {to_address}."
            )
            yes_or_exit(logger=self.app.log.info)
        # Approve
        if self.app.pargs.approve:
            self.app.log.info("Approving DEX to spend token_in...")
            # To approve the transfer of tokens we need the address
            # of the pool. To know the address of the pool, we need
            # the address of the factory, and then call the getPair
            # function of the factory.
            factory_name = self.app.pargs.dex + "_factory"
            factory_contract = Contract.get_by_name_and_chain(
                factory_name, self.app.chain_name
            )
            factory_address = router_client.functions["factory"]().call()
            self.app.log.debug(f"Factory address is {factory_address}")
            # If the factory contract is not in the database, create it
            if not factory_contract:
                self.app.log.debug(
                    f"Factory contract not found, creating it with name {factory_name}..."
                )
                factory_contract = Contract.create(
                    name=factory_name,
                    desc=f"Factory of {self.app.pargs.dex}",
                    chain=self.app.chain_name,
                    address=factory_address,
                    type="uniswap_v2_factory",
                )
            else:
                self.app.log.debug(
                    f"Factory contract found with name {factory_name}..."
                )
                # Throw error if the factory address is different
                if factory_contract.address != factory_address:
                    raise Exception(
                        f"Factory address in database ({factory_contract.address}) is different from the one in the contract ({factory_address})"
                    )
            # Get the pair address
            factory_client = make_contract_client(self.app, factory_name)
            pool_address = factory_client.functions["getPair"](
                token_in, token_out
            ).call()
            self.app.log.debug(f"Pool address is {pool_address}")
            pool_name = f"{self.app.pargs.dex}_{self.app.pargs.token_in}_{self.app.pargs.token_out}"
            pool_contract = Contract.get_by_name_and_chain(
                pool_name, self.app.chain_name
            )
            # If the pool contract is not in the database, create it
            if not pool_contract:
                self.app.log.debug(
                    f"Pool contract not found, creating it with name {pool_name}..."
                )
                pool_contract = Contract.create(
                    name=pool_name,
                    desc=f"Pool {self.app.pargs.token_in}/{self.app.pargs.token_out} of {self.app.pargs.dex}",
                    chain=self.app.chain_name,
                    address=pool_address,
                    type="uniswap_v2_pool",
                )
            else:
                self.app.log.debug(f"Pool contract found with name {pool_name}...")
                # Throw error if the pool address is different
                if pool_contract.address != pool_address:
                    raise Exception(
                        f"Pool address in database ({pool_contract.address}) is different from the one in the contract ({pool_address})"
                    )
            # Check allowance
            allowance = token_in_client.functions["allowance"](
                signer.address, pool_address
            ).call()
            # If allowance is not sufficient, approve
            if allowance < amount_in:
                self.app.log.debug("Approving DEX to spend token_in...")
                approve_function = token_in_client.functions["approve"](
                    pool_address, amount_in
                )
                approve_tx_hash = token_in_client.transact(
                    approve_function, maxPriorityFeePerGasInGwei=self.app.priority_fee
                )
                # Wait for tx to be mined
                self.app.log.debug(f"Approval tx: {approve_tx_hash}")
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
        # Simulate swap
        if self.app.pargs.dry_run:
            self.app.log.debug("Simulating swap...")
            self.app.render(swap_function.call())
            return
        # Swap
        self.app.log.info("Swapping...")
        swap_tx_hash = router_client.transact(
            swap_function, maxPriorityFeePerGasInGwei=self.app.priority_fee
        )
        self.app.print(swap_tx_hash)
