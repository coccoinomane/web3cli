import web3
from web3.contract.contract import ContractFunction
from web3client.base_client import BaseClient

from web3core.constants import ZERO_ADDRESS
from web3core.exceptions import Web3CoreError


def get_swap_function(
    router_client: BaseClient,
    amount_in: int,
    min_amount_out: int,
    token_in: str,
    token_out: str,
    to_address: str,
    deadline: int,
) -> ContractFunction:
    """Return the swap function to use in the router contract.
    Here we account for the fact that some routers have a different
    function signature than the standard Uniswap V2 router."""

    # Standard case: use swapExactTokensForTokens as defined in
    # the Uniswap V2 router ABI
    try:
        return router_client.functions["swapExactTokensForTokens"](
            amount_in, min_amount_out, [token_in, token_out], to_address, deadline
        )
    except web3.exceptions.ABIFunctionNotFound:
        pass

    # Special case: Camelot DEX on Arbitrum One, which has an
    # additional 'referrer' parameter
    # TODO: we could add a contract-level key, "force_referral"
    # or something like that
    try:
        return router_client.functions[
            "swapExactTokensForTokensSupportingFeeOnTransferTokens"
        ](
            amount_in,
            min_amount_out,
            [token_in, token_out],
            to_address,
            ZERO_ADDRESS,
            deadline,
        )
    except web3.exceptions.ABIFunctionNotFound:
        pass

    raise Web3CoreError(
        "Could not find a suitable swap function in the router contract"
    )
