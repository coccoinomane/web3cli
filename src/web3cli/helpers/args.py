import argparse
import json
import os
from typing import Any, List, Literal, Tuple, Union

from web3.types import ABI

from web3cli.exceptions import SignerNotResolved, Web3CliError
from web3cli.framework.app import App
from web3cli.helpers.signer import get_signer
from web3core.exceptions import RpcIsInvalid
from web3core.helpers.blocks import BLOCK_PREDEFINED_IDENTIFIERS, get_block_type
from web3core.helpers.rpc import is_rpc_uri_valid
from web3core.models.chain import Chain, Rpc
from web3core.models.signer import Signer
from web3core.types import TX_LIFE_PROPERTIES, TxLifeProperty

ReturnArg = Union[TxLifeProperty, Literal["all"]]


#  ____
# |  _ \    __ _   _ __   ___    ___
# | |_) |  / _` | | '__| / __|  / _ \
# |  __/  | (_| | | |    \__ \ |  __/
# |_|      \__,_| |_|    |___/  \___|


def pre_parse_args(app: App) -> None:
    """Extend the app object with global arguments. Must be
    run post argument parsing"""

    # If the command requires a chain, save it on the app object
    if hasattr(app.pargs, "chain"):
        app.extend("chain", parse_chain(app))

    # If the command requires a signer, save it on the app object
    # Will ask for password if the signer is given as a keyfile.
    if hasattr(app.pargs, "signer"):
        app.extend("signer", parse_signer(app))

    # If the command requires an rpc, save it on the app object
    if hasattr(app.pargs, "rpc"):
        app.extend("rpc", parse_rpc(app))

    # If the command requires a priority fee, save it on the app object
    if hasattr(app.pargs, "priority_fee"):
        app.extend("priority_fee", parse_priority_fee(app))


def get_command(app: App) -> str:
    """Return the command passed to the CLI, using dot notation.
    For example, if the CLI is invoked as `w3 chain list` the
    function will return the string `chain.list`.

    Return None if the CLI was invoked without a command"""
    try:
        return app.pargs.__dispatch__
    except:
        return None


def parse_chain(app: App) -> Chain:
    """Try to infer which chain the user wants to use,
    and return it as a Chain object.

    The following is the order in which the chain is
    discovered and loaded:

    - Argument --chain or -c passed to the CLI
    - Default chain from the config file
    - If there's only one registered chain, use it

    Otherwise, raise a Web3CliError."""
    if app.pargs.chain:
        chain_name = app.pargs.chain
    elif app.get_option("default_chain"):
        chain_name = app.get_option("default_chain")
    elif Chain.select().count() == 1:
        return Chain.select().get()
    else:
        raise Web3CliError(
            "Could not infer the chain you want to use. Try specifying it with the --chain argument."
        )
    return Chain.get_by_name_or_raise(chain_name)


def parse_rpc(app: App) -> Rpc:
    """Try to infer which RPC the user wants to use,
    and return it as an RPC object.

    The following is the order in which the chain is
    discovered and loaded:

    - Argument --rpc with the RPC url is passed to the CLI
    - Use default RPC for the chain"""
    if not app.pargs.rpc:
        return app.chain.pick_rpc()
    if not is_rpc_uri_valid(app.pargs.rpc):
        raise RpcIsInvalid(f"Given RPC is not valid: {app.pargs.rpc}")
    return Rpc(url=app.pargs.rpc)


def parse_signer(app: App) -> Signer:
    """Try to infer which signer the user wants to use,
    and return it as a Signer object; will ask for
    password if the signer is given as a keyfile.

    The following is the order in which the signer is
    discovered and loaded:

    - Argument --signer or -s passed to the CLI
    - Default signer from the config file
    - If there's only one signer in the DB, use it

    Otherwise, raise a Web3CliError.
    """
    if app.pargs.signer:
        return get_signer(app, app.pargs.signer)
    elif app.get_option("default_signer"):
        return get_signer(app, app.get_option("default_signer"))
    elif Signer.select().count() == 1:
        return Signer.select().get()
    else:
        raise SignerNotResolved(
            "Please specify a signer with --signer or set a default signer in the config file"
        )


def parse_priority_fee(app: App) -> int:
    """If the --priority-fee argument was passed to the CLI, return it; otherwise,
    return its default value from the config file"""
    if app.pargs.priority_fee:
        priority_fee = app.pargs.priority_fee
    else:
        priority_fee = app.get_option("default_priority_fee")
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
    tx_gas_limit_dest: str = "gas_limit",
) -> Tuple[bool, ReturnArg, bool, int]:
    """Parse the CLI arguments '--dry-run', '--return', '--call' and
    '--gas-limit'.

    These parameters are not independent therefore need to be parsed
    together. The gas limit is generally optional, but this function
    requires it when call=true."""
    dry_run: bool = getattr(app.pargs, dry_run_dest)
    tx_return: ReturnArg = getattr(app.pargs, tx_return_dest)
    tx_call: bool = getattr(app.pargs, tx_call_dest)
    tx_gas_limit: bool = getattr(app.pargs, tx_gas_limit_dest)
    # Dry run is incompatibile with certain return values
    if tx_return in ["data", "receipt"] and dry_run:
        raise Web3CliError(
            f"Cannot return '{tx_return}' with 'dry_run' option. Please choose one or the other."
        )
    # Force 'call' mode when function output is requested
    if tx_return == "output" and not tx_call:
        tx_call = True
    # You need to specify a gas limit when call=false
    if not tx_call and not tx_gas_limit:
        raise Web3CliError(
            "Specify a gas limit with '--no-call', otherwise you'll end up with a function call anyway to estimate gas."
        )

    return (dry_run, tx_return, tx_call, tx_gas_limit)


def parse_contract_abi(app: App) -> ABI:
    """Parse the --abi argument passed to the CLI, be it a string or a file,
    and return it as a list of dicts"""
    abi = app.pargs.abi
    if os.path.isfile(abi):
        with open(abi, "r", encoding="utf-8") as f:
            abi = f.read()
    try:
        abi = json.loads(abi)
    except:
        raise Web3CliError("Invalid ABI")
    return abi


#     _
#    / \     _ __    __ _   ___
#   / _ \   | '__|  / _` | / __|
#  / ___ \  | |    | (_| | \__ \
# /_/   \_\ |_|     \__, | |___/
#                   |___/


def block(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["-b", "--block"],
        {
            "help": "Block identifier. Can be an integer, an hex string, or one beetween: "
            + ", ".join(BLOCK_PREDEFINED_IDENTIFIERS),
            "default": "latest",
        }
        | kwargs,
    )


def force(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--force"],
        {
            "help": "proceed without asking for confirmation",
            "action": "store_true",
        }
        | kwargs,
    )


def tx_return(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--return"],
        (
            {
                "help": """Requested output, defaults to 'hash'. Can be one of:
                'hash' will print the transaction hash;
                'params' will print the tx sent to the blockchain;
                'sig' will print the signed transaction object;
                'output' will force a dry run and print the return value of the function;
                'data' will print the tx after it was sent to the blockchain;
                'receipt' will wait for the tx receipt and print it;
                'all' will print all the above.
            """,
                "choices": TX_LIFE_PROPERTIES + ["all"],
                "default": "hash",
            }
            | kwargs
        ),
    )


def tx_dry_run(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--dry-run"],
        {
            "help": "Stop before sending the transaction to the blockchain",
            "action": argparse.BooleanOptionalAction,
            "default": False,
        }
        | kwargs,
    )


def tx_call(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--call"],
        (
            {
                "help": """
                Call the contract function with eth_call, before sending it.
                Useful to test the tx without spending gas
            """,
                "action": argparse.BooleanOptionalAction,
                "default": True,
            }
            | kwargs
        ),
    )


def tx_gas_limit(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--gas-limit"],
        (
            {
                "help": """
                Gas limit to use for the transaction. If not specified, it will
                be estimated by simulating a function call. Usually, you need to
                specify the gas limit only if in conjunction with the --no-call
                option.
            """,
                "type": int,
            }
            | kwargs
        ),
    )


def swap_dex(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["dex"],
        (
            {
                "help": """
                Decentralized Exchange to use for the swap.
                Only Uniswap V2 clones supported for now.
                To see full list: `w3 contract list uniswap_v2`.
            """,
            }
            | kwargs
        ),
    )


def swap_token_in(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["token_in"],
        {
            "help": "Ticker or Address of the token to swap from, e.g. USDC.",
        }
        | kwargs,
    )


def swap_amount(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["amount"],
        {
            "help": "Amount of tokens to swap, e.g. 100.",
            "type": float,
        }
        | kwargs,
    )


def swap_token_out(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["token_out"],
        {
            "help": "Ticker or Address of the token to swap to, e.g. WETH.",
        }
        | kwargs,
    )


def swap_slippage(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--slippage"],
        {
            "help": "Slippage tolerance for the swap, as a percentage. Must be between 0 and 100, defaults to 2.",
            "type": float,
            "default": 2,
        }
        | kwargs,
    )


def swap_min_out(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--min-out"],
        {
            "help": "Minimum amount of tokens to receive. If the swap would result in less tokens, the swap will fail.",
            "type": float,
        }
        | kwargs,
    )


def swap_to(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--to"],
        {
            "help": "Address to send the output tokens to. Defaults to the address of the signer.",
        }
        | kwargs,
    )


def swap_approve(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--approve"],
        {
            "help": "Whether to approve the contract to spend the input token",
            "action": argparse.BooleanOptionalAction,
            "default": True,
        }
        | kwargs,
    )


def swap_deadline(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--deadline"],
        {
            "help": "Deadline for the swap, in seconds. If the swap is not executed before the deadline, it will fail. Defaults to 15 minutes.",
            "default": 15 * 60,
        }
        | kwargs,
    )


def contract_abi(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--abi"],
        {
            "help": "ABI of the contract. Can be a path to a file, or a JSON string.",
        }
        | kwargs,
    )


def priority_fee(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--priority-fee", "--tip"],
        {
            "help": "max priority fee (tip) in gwei you are willing to spend for a transaction",
            "type": int,
            "default": 1,
        }
        | kwargs,
    )


def signer(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["-s", "--signer"],
        {
            "help": "who is going to sign the transaction: a registered signer, a private key, or a keyfile json. Will use the default signer if not specified",
        }
        | kwargs,
    )


def chain(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["-c", "--chain"],
        {
            "help": "chain to use, will use the default chain if not specified",
        }
        | kwargs,
    )


def rpc(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--rpc"],
        {
            "help": "use this RPC url. If not specified, will use the default RPC for the chain ",
        }
        | kwargs,
    )


def callback(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--callback"],
        {
            "help": "Function to call when stuff happens. Available callbacks: print, telegram",
            "default": "print",
        }
        | kwargs,
    )


def subscribe_telegram(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--telegram", "--tg"],
        {
            "help": "Send notifications via Telegram to the given chat ID.  Leave the chat ID blank to use the one defined in the config.  More details in the Github wiki.",
            "nargs": "?",
            "const": "config",
        }
        | kwargs,
    )


def subscribe_post(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--post", "--webhook"],
        {
            "help": "Send a post notifications to this URL.  The body will be a JSON with fields: notification_data, notification_type and tx_data.  The latter field will be populated only when the --senders/--from argument is provided.",
            "nargs": 1,
        }
        | kwargs,
    )


def subscribe_print(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--print"],
        {
            "help": "Print notifications to screen",
            "action": argparse.BooleanOptionalAction,
            "default": True,
        }
        | kwargs,
    )


def subscribe_senders(
    *name_or_flags: str, **kwargs: Any
) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--senders", "--from"],
        {
            "help": "Consider only transactions initiated by these addresses.  Will result in many requests to the node.",
            "nargs": "+",
            "default": [],
        }
        | kwargs,
    )


def tg_message(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--message"],
        {
            "help": "Message to send to the Telegram chat.  Use {data} to place the notification data in the message.",
            "default": "🚨 *New notification from web3cli:*\n\n{data}",
        }
        | kwargs,
    )


def tg_silent(*name_or_flags: str, **kwargs: Any) -> Tuple[List[str], dict[str, Any]]:
    return (
        list(name_or_flags) or ["--silent"],
        {
            "help": "Whether the Telegram notification should produce sound or vibration.",
            "action": "store_true",
        }
        | kwargs,
    )


def tg_args() -> List[Tuple[List[str], dict[str, Any]]]:
    """Shortcut for commands that send Telegram notifications"""
    return [tg_message(), tg_silent()]


def subscribe_actions() -> List[Tuple[List[str], dict[str, Any]]]:
    """Shortcut for commands that trigger actions"""
    return [
        subscribe_telegram(),
        subscribe_post(),
        subscribe_print(),
    ]


def signer_and_gas() -> List[Tuple[List[str], dict[str, Any]]]:
    """Shortcut for commands accepting both signer and gas arguments"""
    return [signer(), priority_fee()]


def tx_args() -> List[Tuple[List[str], dict[str, Any]]]:
    """Shortcut for commands that want to use the
    send_contract_tx helper function"""
    return [tx_return(), tx_dry_run(), tx_call(), tx_gas_limit()]


def chain_and_rpc() -> List[Tuple[List[str], dict[str, Any]]]:
    """Shortcut for commands accepting both chain and rpc arguments"""
    return [chain(), rpc()]


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
