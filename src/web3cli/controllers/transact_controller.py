import web3
from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.exceptions import Web3CliError
from web3cli.helpers.chain import chain_ready_or_raise
from web3cli.helpers.client_factory import make_contract_wallet
from web3cli.helpers.signer import signer_ready_or_raise
from web3core.helpers.abi import parse_abi_values
from web3core.helpers.resolve import resolve_address


class TransactController(Controller):
    """Handler of the `w3 transact` top-level commands"""

    class Meta:
        label = "transact"
        stacked_type = "embedded"
        stacked_on = "base"

    @ex(
        help="Execute a function in the given smart contract and, by default, return the transaction ID. This will cost gas and write to the blockchain. Please use `w3 send` if you just need to send tokens around, as it is less error prone. To see the list of functions in a given contract, run `w3 abi functions <contract>`.",
        arguments=[
            (["contract"], {"action": "store"}),
            (["function"], {"action": "store"}),
            (["args"], {"action": "store", "nargs": "*"}),
        ],
        aliases=["exec"],
    )
    def transact(self) -> None:
        chain_ready_or_raise(self.app)
        signer_ready_or_raise(self.app)
        # Try to fetch the function from the ABI
        client = make_contract_wallet(self.app, self.app.pargs.contract)
        functions = client.functions
        try:
            function = functions[self.app.pargs.function]
        except web3.exceptions.ABIFunctionNotFound:
            raise Web3CliError(f"Function must be one of: {', '.join(functions)}")
        # Parse function args
        function_args = parse_abi_values(
            self.app.pargs.args,
            client.contract.abi,
            self.app.pargs.function,
            checksum_addresses=True,
            resolve_address_fn=lambda x: resolve_address(x, chain=self.app.chain_name),
            allow_exp_notation=True,
        )
        # Execute the function
        tx_hash = client.transact(function(*function_args))
        self.app.print(str(tx_hash))
