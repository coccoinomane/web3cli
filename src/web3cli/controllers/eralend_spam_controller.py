from time import sleep

from cement import ex

from web3cli.controllers.subscribe_controller import SubscribeController
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.tx import send_contract_tx


class EralendSpamController(SubscribeController):
    """Handler of the `w3 eralend-spam` commands"""

    class Meta:
        label = "eralend-spam"
        help = (
            "Try to redeem USDC from the Eralend nUSDC pool, by repaying your own debt"
        )
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="Repay & redeem.  Use flags --no-call --gas-limit 3_000_000",
        arguments=[
            (["amount"], {"help": "Amount of USDC to repay, in wei", "type": int}),
            (
                ["--n"],
                {
                    "help": "Number of spam attempts",
                    "type": int,
                    "default": 3,
                },
            ),
            (
                ["--interval"],
                {
                    "help": "Interval between spam-redeems, in seconds",
                    "type": float,
                    "default": 0.0,
                },
            ),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            *args.tx_args(),
        ],
    )
    def repay_and_spam(self) -> None:
        signer = make_contract_wallet(self.app, "nusdc")
        # Get nonce
        nonce = signer.get_nonce()
        # Repay
        amount = self.app.pargs.amount
        repay_tx = send_contract_tx(
            self.app, signer, signer.functions["repayBorrow"](amount), nonce=nonce
        )
        nonce += 1
        self.app.log.info(f"Repaid: {repay_tx}")
        # Spam-redeem
        for i in range(1, self.app.pargs.n + 1):
            try:
                redeem_tx = send_contract_tx(
                    self.app,
                    signer,
                    signer.functions["redeemUnderlying"](amount),
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
