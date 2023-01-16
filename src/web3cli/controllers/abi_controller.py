import argparse

from cement import ex

from web3cli.controllers.controller import Controller
from web3core.helpers.abi import (
    filter_abi_by_type_and_name,
    get_event_full_signatures,
    get_event_signatures,
    get_function_full_signatures,
    get_function_signatures,
)
from web3core.models.contract import Contract


class AbiController(Controller):
    """Handler of the `w3 abi` commands"""

    class Meta:
        label = "abi"
        help = "extract info about a contract's functions and events"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="List of functions in the given contract, with signatures",
        arguments=[
            (["contract"], {"help": "Name of the contract to inspect"}),
            (
                ["--full", "-f"],
                {
                    "help": "Show full signatures (with parameter types)",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
        ],
        aliases=["fns"],
    )
    def functions(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.contract, self.app.chain_name
        )
        functions = (
            get_function_full_signatures(contract.resolve_abi())
            if self.app.pargs.full
            else get_function_signatures(contract.resolve_abi())
        )
        self.app.render(sorted(functions, key=str.lower))

    @ex(
        help="List of events in the given contract, with signatures",
        arguments=[
            (["contract"], {"help": "Name of the contract to inspect"}),
            (
                ["--full", "-f"],
                {
                    "help": "Show full signatures (with parameter types)",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
        ],
        aliases=["evts"],
    )
    def events(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.contract, self.app.chain_name
        )
        events = (
            get_event_full_signatures(contract.resolve_abi())
            if self.app.pargs.full
            else get_event_signatures(contract.resolve_abi())
        )
        self.app.render(sorted(events, key=str.lower))

    @ex(
        help="Show the ABI of a specific contract function or event",
        arguments=[
            (["contract"], {"help": "Name of the contract to inspect"}),
            (["name"], {"help": "Name of the function or event"}),
        ],
    )
    def get(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.contract, self.app.chain_name
        )
        abi = contract.resolve_abi()
        self.app.render(
            filter_abi_by_type_and_name(abi, type=None, name=self.app.pargs.name),
            indent=4,
            handler="json",
        )
