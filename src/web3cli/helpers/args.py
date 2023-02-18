import argparse
from typing import Any, Literal, Tuple, Union

from cement import App

from web3cli.exceptions import Web3CliError
from web3core.exceptions import RpcIsInvalid
from web3core.helpers.blocks import BLOCK_PREDEFINED_IDENTIFIERS, get_block_type
from web3core.helpers.rpc import is_rpc_uri_valid
from web3core.models.chain import Chain
from web3core.models.signer import Signer
from web3core.types import TX_LIFE_PROPERTIES, TxLifeProperty

ReturnArg = Union[TxLifeProperty, Literal["all"]]


#  ____
# |  _ \    __ _   _ __   ___    ___
# | |_) |  / _` | | '__| / __|  / _ \
# |  __/  | (_| | | |    \__ \ |  __/
# |_|      \__,_| |_|    |___/  \___|


def parse_global_args(app: App) -> None:
    """Extend the app object with global arguments. Must be
    run post argument parsing"""

    app.extend("signer", parse_signer(app))
    app.extend("priority_fee", parse_priority_fee(app))
    app.extend("rpc", parse_rpc(app))
    app.extend("chain_name", parse_chain(app))
    app.extend("chain", Chain.get_by_name(app.chain_name))


def get_command(app: App) -> str:
    """Return the command passed to the CLI, using dot notation.
    For example, if the CLI is invoked as `w3 db chain list` the
    function will return the string `chain.list`.

    Return None if the CLI was invoked without a command"""
    try:
        return app.pargs.__dispatch__
    except:
        return None


def parse_chain(app: App) -> str:
    """Try to infer which chain the user wants to use.

    The following is the order in which the chain is
    discovered and loaded:

    - Argument --chain or -c passed to the CLI
    - Default chain from the config file
    - If there's only one chain in the DB, use it

    Otherwise, raise a Web3CliError."""
    if app.pargs.chain:
        chain = app.pargs.chain
    elif Chain.select().count() == 1:
        chain = Chain.select().get().name
    elif app.config.get("web3cli", "default_chain"):
        chain = app.config.get("web3cli", "default_chain")
    else:
        raise Web3CliError(
            "Could not infer the chain you want to use. Try specifying it with the --chain argument."
        )
    return chain


def parse_rpc(app: App) -> str:
    """If the argument --rpc was passed to the CLI, return it; otherwise,
    return None, in which case the app will automatically determine the
    best RPC to use based on the selected chain"""
    if not app.pargs.rpc:
        return None
    if not is_rpc_uri_valid(app.pargs.rpc):
        raise RpcIsInvalid(f"Given RPC is not valid: {app.pargs.rpc}")
    return app.pargs.rpc


def parse_signer(app: App) -> str:
    """Try to infer which signer the user wants to use.

    The following is the order in which the signer is
    discovered and loaded:

    - Argument --signer or -s passed to the CLI
    - Default signer from the config file
    - If there's only one signer in the DB, use it

    Otherwise, return None, and leave to the app the
    responsibility to raise an error. We do not raise
    it here because we don't know yet whether the command
    invoked by the user really needs a signer.
    """
    if app.pargs.signer:
        signer = app.pargs.signer
    elif app.config.get("web3cli", "default_signer"):
        signer = app.config.get("web3cli", "default_signer")
    elif Signer.select().count() == 1:
        signer = Signer.select().get().name
    else:
        signer = None
    return signer


def parse_priority_fee(app: App) -> int:
    """If the --priority-fee argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.priority_fee:
        priority_fee = app.pargs.priority_fee
    else:
        priority_fee = app.config.get("web3cli", "default_priority_fee")
    if not priority_fee:
        raise Web3CliError("Priority fee not defined, should not be here")
    return priority_fee


def parse_block(app: App, label: str = "block") -> Union[str, int]:
    """Return the block number or hash passed to the CLI, converted
    to the proper type (int if number, str if hash)"""
    # Is it a number, a hash or a predefined identifier?
    value = getattr(app.pargs, label)
    try:
        block_type = get_block_type(value)
    except:
        raise Web3CliError(
            f"Invalid block identifier '{value}', must be either an integer, an hex string, or one beetween "
            + ", ".join(BLOCK_PREDEFINED_IDENTIFIERS)
        )
    # Non numeric blocks are returned as is, no conversion needed
    if block_type != "number":
        return value
    # Numeric blocks are converted to int
    try:
        return int(value)
    except:
        return int(value, 16)


def parse_tx_args(
    app: App,
    dry_run_dest: str = "dry_run",
    tx_return_dest: str = "return",
    tx_call_dest: str = "call",
) -> Tuple[bool, ReturnArg, bool]:
    """Parse the CLI arguments '--dry-run', '--return' and '--call'.

    These parameters are not independent therefore need to be parsed
    together."""
    dry_run: bool = getattr(app.pargs, dry_run_dest)
    tx_return: ReturnArg = getattr(app.pargs, tx_return_dest)
    tx_call: bool = getattr(app.pargs, tx_call_dest)
    # Handle incompatibilities between options
    if tx_return in ["data", "receipt"] and (dry_run or tx_call):
        flag = dry_run_dest if dry_run else tx_call_dest
        raise Web3CliError(
            f"Cannot return '{tx_return}' with '{flag}' option. Please choose one or the other."
        )
    # Force 'call' mode when function output is requested
    if tx_return == "output" and not tx_call:
        tx_call = True

    return (dry_run, tx_return, tx_call)


#     _
#    / \     _ __    __ _   ___
#   / _ \   | '__|  / _` | / __|
#  / ___ \  | |    | (_| | \__ \
# /_/   \_\ |_|     \__, | |___/
#                   |___/


def block(**kwargs: Any) -> dict[str, Any]:
    """The 'block' argument, used to specify a block number or hash"""
    return {
        "help": "Block identifier. Can be an integer, an hex string, or one beetween: "
        + ", ".join(BLOCK_PREDEFINED_IDENTIFIERS),
        "action": "store",
        "default": "latest",
    } | kwargs


def force(**kwargs: Any) -> dict[str, Any]:
    """The 'force' argument, used to force a command to run without asking for
    confirmation"""
    return {
        "help": "Proceed without asking for confirmation",
        "action": "store_true",
    } | kwargs


def tx_return(**kwargs: Any) -> dict[str, Any]:
    """The 'return' argument, used to choose what to return from a
    transaction"""
    return (
        {
            "help": """Requested output.
                'hash' will print the transaction hash,
                'params' will print the tx sent to the blockchain,
                'sig' will print the signed transaction object,
                'output' will force a dry run and print the return value of the function,
                'data' will print the tx after it was sent to the blockchain,
                'receipt' will wait for the tx receipt and print it,
                'all' will print all the above
            """,
            "action": "store",
            "choices": TX_LIFE_PROPERTIES + ["all"],
            "default": "hash",
        }
        | kwargs
    )


def tx_dry_run(**kwargs: Any) -> dict[str, Any]:
    """The 'dry_run' argument, to allow the user to avoid sendin the transaction"""
    return {
        "help": "do not send the transaction to the blockchain",
        "action": argparse.BooleanOptionalAction,
        "default": False,
    } | kwargs


def tx_call(**kwargs: Any) -> dict[str, Any]:
    """The 'call' argument, to allow the user to simulate the transaction"""
    return {
        "help": "call the contract function with eth_call, before sending it. Useful to test the tx before sending it.",
        "action": argparse.BooleanOptionalAction,
        "default": False,
    } | kwargs


#  _   _   _     _   _
# | | | | | |_  (_) | |  ___
# | | | | | __| | | | | / __|
# | |_| | | |_  | | | | \__ \
#  \___/   \__| |_| |_| |___/


def override_arg(app: App, arg: str, value: str) -> App:
    """Set the value passed to the given argument, overriding whatever
    value was read from the CLI or inferred from the environment.

    Needs to be called before argument parsing."""

    def post_argument_parsing_callback(a: App) -> None:
        setattr(a.pargs, arg, value)

    app.hook.register("post_argument_parsing", post_argument_parsing_callback)
    return app
