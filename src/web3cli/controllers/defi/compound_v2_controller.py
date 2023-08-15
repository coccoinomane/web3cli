import decimal
from time import sleep
from typing import Tuple

from cement import ex
from web3client.base_client import BaseClient
from web3client.erc20_client import Erc20Client

from web3cli.exceptions import DefiError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import (
    make_contract_client,
    make_contract_wallet,
    make_erc20_client_from_address,
    make_erc20_wallet_from_address,
)
from web3cli.helpers.render import render
from web3cli.helpers.token import approve
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address


class CompoundV2Controller(Controller):
    """Handler of the `w3 compound-v2` commands"""

    class Meta:
        label = "compound-v2"
        help = "Interact with the Compound V2 lending protocol (https://docs.compound.finance/v2/).  It also works with Compound forks, like Eralend on zkSync Era. Requires a Compound pool contract: create one with `w3 contract add <name> <pool address> --type compound_v2_erc20`."
        stacked_type = "nested"
        stacked_on = "base"
        aliases = ["eralend"]

    @ex(
        help="Show amount of debt owed to the given pool by the given address",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (["address"], {"help": "User address to check"}),
            *args.chain_and_rpc(),
        ],
        aliases=["debt"],
    )
    def borrowed(self) -> None:
        pool = make_contract_client(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(pool)
        amount = pool.functions["borrowBalanceStored"](
            resolve_address(self.app.pargs.address)
        ).call()
        render(self.app, amount / decimal.Decimal(10**decimals))

    @ex(
        help="Show total amount of debt owed to the given pool",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            *args.chain_and_rpc(),
        ],
        aliases=["total-debt"],
    )
    def total_borrow(self) -> None:
        pool = make_contract_client(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(pool)
        amount = pool.functions["totalBorrows"]().call()
        render(self.app, amount / decimal.Decimal(10**decimals))

    @ex(
        help="Show amount of collateral supplied to the given pool by the given address",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (["address"], {"help": "User address to check"}),
            *args.chain_and_rpc(),
        ],
        aliases=["collateral"],
    )
    def supplied(self) -> None:
        pool = make_contract_client(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(pool)
        amount = pool.functions["balanceOfUnderlying"](
            resolve_address(self.app.pargs.address)
        ).call()
        render(self.app, amount / decimal.Decimal(10**decimals))

    @ex(
        help="Show total amount of cTokens in existence for the given pool",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            *args.chain_and_rpc(),
        ],
        aliases=["total-collateral"],
    )
    def total_supply(self) -> None:
        pool = make_contract_client(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(pool)
        amount = pool.functions["totalSupply"]().call()
        render(self.app, amount / decimal.Decimal(10**decimals))

    @ex(
        help="Show total amount of liquid collateral (cash) in the given pool",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            *args.chain_and_rpc(),
        ],
    )
    def liquidity(self) -> None:
        pool = make_contract_client(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(pool)
        amount = pool.functions["getCash"]().call()
        render(self.app, amount / decimal.Decimal(10**decimals))

    @ex(
        help="Repay debt to the given pool",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (
                ["amount"],
                {
                    "help": "Amount of tokens to repay; specify 0 to repay all debt",
                    "type": float,
                },
            ),
            args.swap_approve(
                help="Automatically approve pool to use your tokens.  Ignored for ETH pools."
            ),
            *args.signer_and_gas(),
            *args.tx_args(),
            *args.chain_and_rpc(),
            args.force(),
        ],
    )
    def repay(self) -> None:
        # Get amount in wei
        signer = make_contract_wallet(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(signer)
        amount = self.app.pargs.amount
        amount_in_wei = int(amount * 10**decimals)

        # Allow to repay all debt
        if self.app.pargs.amount == 0:
            amount_in_wei = signer.functions["borrowBalanceStored"](
                signer.user_address
            ).call()
            amount = amount_in_wei / 10**decimals

        # Confirm
        if not self.app.pargs.force:
            print(
                f"You are about to repay {amount} {symbol} to the '{self.app.pargs.contract}' pool"
            )
            yes_or_exit(logger=self.app.log.info)

        if token:
            # Approve token spending
            if self.app.pargs.approve:
                approve(
                    app=self.app,
                    token_client=token,
                    spender=signer.contract_address,
                    amount_in_wei=amount_in_wei,
                    check_allowance=True,
                )
            # Send transaction
            output = send_contract_tx(
                self.app, signer, signer.functions["repayBorrow"](amount_in_wei)
            )
        else:
            # ETH pool: send payable transaction
            output = send_contract_tx(
                self.app,
                signer,
                signer.functions["repayBorrow"](),
                value_in_wei=amount_in_wei,
            )
        render(self.app, output)

    # Withdraw function, similar to repay function:
    @ex(
        help="Withdraw collateral from the given pool.  IMPORTANT: To avoid liquidation, make sure to always leave enough collateral",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (
                ["amount"],
                {
                    "help": "Amount of tokens to withdraw; specify 0 to withdraw all collateral",
                    "type": float,
                },
            ),
            *args.signer_and_gas(),
            *args.tx_args(),
            *args.chain_and_rpc(),
            args.force(),
        ],
    )
    def withdraw(self) -> None:
        # Get amount in wei
        signer = make_contract_wallet(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(signer)
        amount = self.app.pargs.amount
        amount_in_wei = int(amount * 10**decimals)

        # Allow to withdraw all collateral
        if self.app.pargs.amount == 0:
            amount_in_wei = signer.functions["balanceOfUnderlying"](
                signer.user_address
            ).call()
            amount = amount_in_wei / 10**decimals

        # Confirm
        if not self.app.pargs.force:
            print(
                f"You are about to withdraw {amount} {symbol} from the '{self.app.pargs.contract}' pool"
            )
            yes_or_exit(logger=self.app.log.info)

        # Send transaction
        output = send_contract_tx(
            self.app, signer, signer.functions["redeemUnderlying"](amount_in_wei)
        )
        render(self.app, output)

    @ex(
        help="Supply collateral to the given pool",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (["amount"], {"help": "Amount of tokens to supply", "type": float}),
            (
                ["--collateral"],
                {
                    "help": "Whether to enable the pool to be used as collateral",
                    "action": "store_true",
                },
            ),
            args.swap_approve(
                help="Automatically approve pool to use your tokens.  Ignored for ETH pools."
            ),
            *args.signer_and_gas(),
            *args.tx_args(),
            *args.chain_and_rpc(),
            args.force(),
        ],
    )
    def supply(self) -> None:
        if self.app.pargs.collateral:
            raise NotImplementedError(
                f"Flat --collateral to enable collateral not implemented yet"
            )

        # Get amount in wei
        signer = make_contract_wallet(self.app, self.app.pargs.contract)
        token, symbol, decimals = self.get_underlying(signer)
        amount_in_wei = int(self.app.pargs.amount * 10**decimals)

        # Confirm
        if not self.app.pargs.force:
            print(
                f"You are about to supply {self.app.pargs.amount} {symbol} to the '{self.app.pargs.contract}' pool"
            )
            yes_or_exit(logger=self.app.log.info)

        if token:
            # Approve token spending
            if self.app.pargs.approve:
                approve(
                    app=self.app,
                    token_client=token,
                    spender=signer.contract_address,
                    amount_in_wei=amount_in_wei,
                    check_allowance=True,
                )
            # Send transaction
            mint_tx = send_contract_tx(
                self.app, signer, signer.functions["mint"](amount_in_wei)
            )
        else:
            # ETH pool: send payable transaction
            mint_tx = send_contract_tx(
                self.app, signer, signer.functions["mint"](), value_in_wei=amount_in_wei
            )
        render(self.app, mint_tx)

    @ex(
        help="Borrow tokens from the given pool.  IMPORTANT: To avoid liquidation, make sure to borrow within your collateral ratio",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (["amount"], {"help": "Amount of tokens to borrow", "type": float}),
            *args.signer_and_gas(),
            *args.tx_args(),
            *args.chain_and_rpc(),
            args.force(),
        ],
    )
    def borrow(self) -> None:
        # Get amount in wei
        signer = make_contract_wallet(self.app, self.app.pargs.contract)
        _, symbol, decimals = self.get_underlying(signer)
        amount_in_wei = int(self.app.pargs.amount * 10**decimals)
        # Confirm
        if not self.app.pargs.force:
            print(
                f"You are about to borrow {self.app.pargs.amount} {symbol} from the '{self.app.pargs.contract}' pool"
            )
            yes_or_exit(logger=self.app.log.info)
        # Send transaction
        output = send_contract_tx(
            self.app, signer, signer.functions["borrow"](amount_in_wei)
        )
        render(self.app, output)

    @ex(
        help="Recover collateral from an empty Compound pool, by repaying your own debt and, immediately after, redeeming",
        arguments=[
            (["contract"], {"help": "Name of the pool contract"}),
            (["amount"], {"help": "Amount of tokens to repay", "type": float}),
            (
                ["--n"],
                {
                    "help": "Number of redeem attempts",
                    "type": int,
                    "default": 3,
                },
            ),
            (
                ["--interval"],
                {
                    "help": "Interval between redeem attempts, in seconds",
                    "type": float,
                    "default": 0.0,
                },
            ),
            *args.tx_args(),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            args.force(),
        ],
    )
    def recover(self) -> None:
        # Get amount in wei
        signer = make_contract_wallet(self.app, self.app.pargs.contract)
        underlying = Erc20Client(
            self.app.rpc.url, contract_address=signer.functions["underlying"]().call()
        )
        amount = self.app.pargs.amount
        amount_in_wei = int(amount * 10**underlying.decimals)
        # We must have at least 'amount' of both debt and borrow
        debt_balance = signer.functions["borrowBalanceStored"](
            signer.user_address
        ).call()
        self.app.log.info(
            f"Your debt is {debt_balance/10**underlying.decimals} {underlying.symbol}"
        )
        supply_balance = signer.functions["balanceOfUnderlying"](
            signer.user_address
        ).call()
        self.app.log.info(
            f"Your collateral is {supply_balance/10**underlying.decimals} {underlying.symbol}"
        )
        # Adjust amount
        if amount_in_wei > debt_balance or amount_in_wei > supply_balance:
            amount_in_wei = min(amount_in_wei, debt_balance, supply_balance)
            amount = amount_in_wei / 10**underlying.decimals
            self.app.log.info(
                f"Recover amount too high: reduced to {amount} {underlying.symbol}"
            )
        # Let's not waste time
        if amount_in_wei < 1:
            raise DefiError(f"Amount too small: {amount}")
        # Confirm
        if not self.app.pargs.force:
            print(f"You are about to:")
            print(
                f" 1. repay {amount} {underlying.symbol} to the '{self.app.pargs.contract}' pool"
            )
            print(
                f" 2. attempt to redeem the same amount as quick as possible, for {self.app.pargs.n} times"
            )
            yes_or_exit(logger=self.app.log.info)
        # Get nonce
        nonce = signer.get_nonce()
        # Force no call simulation
        self.app.pargs.call = False
        # Repay
        repay_tx = send_contract_tx(
            self.app,
            signer,
            signer.functions["repayBorrow"](amount_in_wei),
            nonce=nonce,
        )
        nonce += 1
        self.app.log.info(f"Repaid: {repay_tx}")
        # Spam-redeem
        for i in range(1, self.app.pargs.n + 1):
            try:
                redeem_tx = send_contract_tx(
                    self.app,
                    signer,
                    signer.functions["redeemUnderlying"](amount_in_wei),
                    nonce=nonce,
                )
            except Exception as e:
                self.app.log.warning(f"Attempt {i}: Error in spamming: {e}")
                if self.app.pargs.interval > 0:
                    sleep(self.app.pargs.interval)
                continue

            nonce += 1
            self.app.log.info(f"Attempt {i}: tx sent: {redeem_tx}")
            if self.app.pargs.interval > 0:
                sleep(self.app.pargs.interval)

    def get_underlying(self, pool: BaseClient) -> Tuple[BaseClient, str, int]:
        """Return underlying token client, symbol and decimals.  For ETH pools,
        the token client will be None."""

        # Case of ETH pool
        if not hasattr(pool.functions, "underlying"):
            return None, "ETH", 18

        # Case of ERC20 pool
        underlying_address = pool.functions["underlying"]().call()
        if hasattr(self.app.pargs, "signer"):
            token_client = make_erc20_wallet_from_address(self.app, underlying_address)
        else:
            token_client = make_erc20_client_from_address(self.app, underlying_address)
        return (
            token_client,
            token_client.functions["symbol"]().call(),
            token_client.functions["decimals"]().call(),
        )
