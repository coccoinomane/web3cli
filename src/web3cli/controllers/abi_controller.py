from cement import ex

from web3cli.controllers.controller import Controller
from web3core.helpers.abi import abi_to_function_signatures
from web3core.models.contract import Contract


class AbiController(Controller):
    """Handler of the `w3 abi` commands"""

    class Meta:
        label = "abi"
        help = "extract info about a contract's functions and events"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="List of functions signatures in the given contract",
        arguments=[(["contract"], {"action": "store"})],
    )
    def functions(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.contract, self.app.chain_name
        )
        functions = abi_to_function_signatures(contract.resolve_abi())
        self.app.render(sorted(functions, key=str.lower))
