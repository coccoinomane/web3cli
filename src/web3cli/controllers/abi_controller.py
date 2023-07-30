import argparse

from cement import ex
from web3.types import ABI

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render
from web3core.helpers.abi import decode_function_data as _decode_function_data
from web3core.helpers.abi import (
    filter_abi_by_type_and_name,
    get_event_full_signatures,
    get_event_signatures,
    get_function_full_signatures,
    get_function_signatures,
)
from web3core.helpers.contract import get_web3_contract
from web3core.models.contract import Contract, ContractType


class AbiController(Controller):
    """Handler of the `w3 abi` commands"""

    class Meta:
        label = "abi"
        help = "extract info about a contract's functions and events"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="List the functions in the given contract, contract type or ABI string, with signatures",
        arguments=[
            (
                ["contract"],
                {
                    "help": "Name of the contract or contract type in the database",
                    "nargs": "?",
                },
            ),
            args.contract_abi(
                help="Pass the ABI of the contract instead, as a string or file"
            ),
            (
                ["--full", "-f"],
                {
                    "help": "Show full signatures (with parameter types)",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
            args.chain(),
        ],
        aliases=["fns", "fn", "f"],
    )
    def functions(self) -> None:
        abi = self.parse_abi()
        functions = (
            get_function_full_signatures(abi)
            if self.app.pargs.full
            else get_function_signatures(abi)
        )
        render(self.app, sorted(functions, key=str.lower))

    @ex(
        help="List the events in the given contract, contract type or ABI string, with signatures",
        arguments=[
            (
                ["contract"],
                {
                    "help": "Name of the contract or contract type in the database.",
                    "nargs": "?",
                },
            ),
            args.contract_abi(
                help="Pass the ABI of the contract instead, as a string or file"
            ),
            (
                ["--full", "-f"],
                {
                    "help": "Show full signatures (with parameter types)",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
            args.chain(),
        ],
        aliases=["evs", "ev", "e"],
    )
    def events(self) -> None:
        abi = self.parse_abi()
        events = (
            get_event_full_signatures(abi)
            if self.app.pargs.full
            else get_event_signatures(abi)
        )
        render(self.app, sorted(events, key=str.lower))

    @ex(
        help="Show the ABI of a specific contract function or event",
        arguments=[
            (
                ["contract"],
                {"help": "Name of the contract or contract type in the database"},
            ),
            (["function_name"], {"help": "Name of the function or event"}),
            args.chain(),
        ],
    )
    def get(self) -> None:
        abi = self.parse_abi()
        obj = filter_abi_by_type_and_name(
            abi, type=None, name=self.app.pargs.function_name
        )
        if not obj:
            self.app.log.warning(
                f"Function or event '{self.app.pargs.function_name}' not found"
            )
        render(self.app, obj)

    @ex(
        help="Given input data for a contract function, return its decoded arguments and, optionally, the function signature",
        arguments=[
            (["contract"], {"help": "Name of the contract"}),
            (["data"], {"help": "Input data"}),
            (
                ["--name"],
                {"help": "Specify the function name rather than its selector"},
            ),
            (
                ["--signature"],
                {
                    "help": "Include function signature in the output, with key __function_signature",
                    "action": "store_true",
                },
            ),
            args.chain(),
        ],
    )
    def decode_function_data(self) -> None:
        web3_contract = get_web3_contract(self.app.pargs.contract, self.app.chain)
        params, signature = _decode_function_data(
            web3_contract.abi, self.app.pargs.data, self.app.pargs.name
        )
        if self.app.pargs.signature:
            params["__function_signature"] = signature
        render(self.app, params)

    def parse_abi(self) -> ABI:
        """Parse the 'contract' and '--abi' arguments and return the ABI"""
        # Contract name given, try to retrieve the ABI from the database
        if self.app.pargs.contract:
            # Try to retrieve ABI from contracts table
            contract = Contract.get_by_name_and_chain(
                self.app.pargs.contract, self.app.chain.name
            )
            if contract:
                return contract.resolve_abi()
            # Try to retrieve ABI from contract_types table
            contract_type = ContractType.get_by_name(self.app.pargs.contract)
            if contract_type:
                return contract_type.abi
            # Contract not found
            raise Web3CliError(f"Contract {self.app.pargs.contract} not found")
        # No contract name given, try to parse the ABI as string or file
        if self.app.pargs.abi:
            return args.parse_contract_abi(self.app)
        # Should never happen
        raise Web3CliError("ABI not found")
