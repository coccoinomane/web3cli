import argparse
import decimal

from cement import ex

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.client_factory import make_contract_client, make_contract_wallet
from web3cli.helpers.render import render, render_table
from web3cli.helpers.tx import send_contract_tx
from web3core.helpers.misc import yes_or_exit
from web3core.helpers.resolve import resolve_address
from web3core.models.contract import Contract


class TokenController(Controller):
    """Handler of the `w3 token` command"""

    class Meta:
        label = "token"
        help = "interact with ERC20 tokens"
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
                    "help": "Amount of tokens to approve. Leave empty to approve the maximum amount",
                    "type": float,
                    "nargs": "?",
                },
            ),
            (
                ["--check"],
                {
                    "help": "Whether to stop if the spender already has enough allowance",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
            *args.tx_args(),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            args.force(),
        ],
    )
    def approve(self) -> None:
        # Parse arguments
        spender = resolve_address(self.app.pargs.spender, chain=self.app.chain.name)
        # Initialize client
        signer = make_contract_wallet(self.app, self.app.pargs.token)
        # Compute amount in
        if not self.app.pargs.amount:
            amount_in_wei = 2**256 - 1
        else:
            decimals = signer.functions["decimals"]().call()
            amount_in_wei = int(self.app.pargs.amount * 10**decimals)
        # Approve
        if self.app.pargs.check:
            self.app.log.debug("Checking token allowance...")
            allowance = signer.functions["allowance"](
                self.app.signer.address, spender
            ).call()
            # If allowance is not sufficient, approve
            if allowance >= amount_in_wei:
                self.app.log.info(
                    f"Token allowance already sufficient {allowance} >= {amount_in_wei}"
                )
                return
        # Confirm
        if not self.app.pargs.force:
            what = (
                (str(self.app.pargs.amount) if self.app.pargs.amount else "infinite")
                + " "
                + self.app.pargs.token
            )
            print(
                f"You are about to approve {spender} on chain {self.app.chain.name} to spend {what} on behalf of {signer.user_address}"
            )
            yes_or_exit(logger=self.app.log.info)
        self.app.log.debug("Approving spender to spend token...")
        output = send_contract_tx(
            self.app,
            signer,
            signer.functions["approve"](spender, amount_in_wei),
        )
        # Print output
        render(self.app, output)

    @ex(
        help="Revoke spending permissions from the given spender",
        arguments=[
            (["token"], {"help": "Token to approve"}),
            (["spender"], {"help": "Address or name of the spender to be revoked"}),
            *args.tx_args(),
            *args.chain_and_rpc(),
            *args.signer_and_gas(),
            args.force(),
        ],
    )
    def revoke(self) -> None:
        spender = resolve_address(self.app.pargs.spender, chain=self.app.chain.name)
        signer = make_contract_wallet(self.app, self.app.pargs.token)
        # Confirm
        if not self.app.pargs.force:
            print(
                f"Revoke permissions to {spender} on chain {self.app.chain.name} to spend on behalf of {signer.user_address}?"
            )
            yes_or_exit(logger=self.app.log.info)
        self.app.log.debug("Revoking spender to spend token...")
        output = send_contract_tx(
            self.app,
            signer,
            signer.functions["approve"](spender, 0),
        )
        # Print output
        render(self.app, output)

    @ex(
        help="Show the balance of the given token for the given address",
        arguments=[
            (["token"], {"help": "Token to check, by name"}),
            (["address"], {"help": "Address or name of the account to check"}),
            (["--wei"], {"help": "Print the output in wei", "action": "store_true"}),
            *args.chain_and_rpc(),
        ],
    )
    def balance(self) -> None:
        address = resolve_address(self.app.pargs.address, chain=self.app.chain.name)
        client = make_contract_client(self.app, self.app.pargs.token)
        balance_in_wei = client.functions["balanceOf"](address).call()
        if self.app.pargs.wei:
            render(self.app, balance_in_wei)
        else:
            balance = balance_in_wei / decimal.Decimal(
                10 ** client.functions["decimals"]().call()
            )
            render(self.app, balance)

    @ex(
        help="Return the allowance of the given spender to spend the given token for the given address",
        arguments=[
            (["token"], {"help": "Token to check, by name"}),
            (["owner"], {"help": "Address or name of the account to check"}),
            (["spender"], {"help": "Address or name of the spender to check"}),
            *args.chain_and_rpc(),
        ],
    )
    def allowance(self) -> None:
        # Parse arguments
        spender = resolve_address(self.app.pargs.spender, chain=self.app.chain.name)
        owner = resolve_address(self.app.pargs.owner, chain=self.app.chain.name)
        # Initialize client
        client = make_contract_client(self.app, self.app.pargs.token)
        decimals = client.functions["decimals"]().call()
        allowance_in_wei = client.functions["allowance"](owner, spender).call()
        allowance = allowance_in_wei / 10**decimals
        render(self.app, allowance)

    @ex(help="Transfer tokens.  Not implemented yet.  Use `w3 send` instead.")
    def transfer(self) -> None:
        self.app.log.warning("Not implemented yet.  Use `w3 send` instead.")

    #    ____                      _
    #   / ___|  _ __   _   _    __| |
    #  | |     | '__| | | | |  / _` |
    #  | |___  | |    | |_| | | (_| |
    #   \____| |_|     \__,_|  \__,_|

    @ex(
        help="add a new token to the database",
        arguments=[
            (["name"], {"help": "name of the token"}),
            (["-d", "--desc"], {"action": "store"}),
            (
                ["address"],
                {"help": "address of the contract on the blockchain (0x...)"},
            ),
            (
                ["-u", "--update"],
                {
                    "help": "if a contract with the same name is present, overwrite it",
                    "action": "store_true",
                },
            ),
            args.chain(),
        ],
    )
    def add(self) -> None:
        # Add or update contract
        contract = Contract.get_by_name_and_chain(
            self.app.pargs.name, self.app.chain.name
        )
        if not contract or self.app.pargs.update:
            Contract.upsert(
                {
                    "name": self.app.pargs.name,
                    "desc": self.app.pargs.desc,
                    "type": "erc20",
                    "address": self.app.pargs.address,
                    "chain": self.app.chain.name,
                },
                logger=self.app.log.info,
            )
        else:
            raise Web3CliError(
                f"Contract '{self.app.pargs.name}' already exists. Use `--update` or `-u` to update it."
            )

    @ex(help="list tokens registered in the database", arguments=[args.chain()])
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [c.name, c.chain, c.type, "Yes" if bool(c.abi) else "No", c.address]
                for c in Contract.get_all(Contract.name)
                if c.chain == self.app.chain.name and c.type == "erc20"
            ],
            headers=["NAME", "CHAIN", "TYPE", "ABI", "ADDRESS"],
            wrap=42,
        )

    @ex(
        help="delete a token from the database",
        arguments=[(["name"], {"help": "name of the token to delete"}), args.chain()],
    )
    def delete(self) -> None:
        contract = Contract.get_by_name_chain_and_type_or_raise(
            self.app.pargs.name, self.app.chain.name, "erc20"
        )
        contract.delete_instance()
        self.app.log.info(
            f"Contract '{self.app.pargs.name}' on chain '{self.app.chain.name}' deleted correctly"
        )
