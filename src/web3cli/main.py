import configparser
import os
from typing import Callable

import web3
from cement import App, init_defaults
from cement.core.exc import CaughtSignal

from web3cli import hooks
from web3cli.controllers.abi_controller import AbiController
from web3cli.controllers.app_key_controller import AppKeyController
from web3cli.controllers.base_controller import BaseController
from web3cli.controllers.call_controller import CallController
from web3cli.controllers.config_controller import ConfigController
from web3cli.controllers.crud.address_controller import AddressController
from web3cli.controllers.crud.chain_controller import ChainController
from web3cli.controllers.crud.contract_controller import ContractController
from web3cli.controllers.crud.history_controller import HistoryController
from web3cli.controllers.crud.rpc_controller import RpcController
from web3cli.controllers.crud.signer_controller import SignerController
from web3cli.controllers.db_controller import DbController
from web3cli.controllers.keyfile_controller import KeyfileController
from web3cli.controllers.misc_controller import MiscController
from web3cli.controllers.send_controller import SendController
from web3cli.controllers.swap_controller import SwapController
from web3cli.controllers.token_controller import TokenController
from web3cli.controllers.transact_controller import TransactController
from web3cli.controllers.tx_controller import TxController
from web3cli.exceptions import Web3CliError
from web3cli.helpers.args import override_arg
from web3core.exceptions import Web3CoreError

# Configuration defaults
CONFIG = init_defaults("web3cli")
CONFIG["web3cli"] = {
    "app_key": None,
    "debug": False,
    "default_chain": "eth",
    "default_signer": None,
    "default_priority_fee": 1,
    "db_file": os.path.join(
        os.path.expanduser("~"), ".web3cli", "database", "web3cli.sqlite"
    ),
    "output_table_format": "fancy_grid",
    "output_table_wrap": 33,
    "populate_db": True,
}


class Web3Cli(App):
    """Web3 Cli primary application."""

    class Meta:
        label = "web3cli"

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            "yaml",
            "json",
            "colorlog",
            "jinja2",
            "print",
            "tabulate",
        ]

        # configuration handler
        config_handler = "yaml"

        # Path of configuration file(s).
        # The order is important as the later files override
        # the settings in the previous ones.
        config_files = [
            os.path.join(os.path.expanduser("~"), ".web3cli", "config", "web3cli.yml"),
            os.path.join(os.getcwd(), "web3cli.yml"),
        ]

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "yaml"

        # register handlers
        handlers = [
            BaseController,
            ConfigController,
            DbController,
            ChainController,
            RpcController,
            SignerController,
            AddressController,
            HistoryController,
            ContractController,
            AppKeyController,
            MiscController,
            SendController,
            TxController,
            AbiController,
            CallController,
            TransactController,
            SwapController,
            TokenController,
            KeyfileController,
        ]

        # extend the app with cement hook system
        hooks = [
            ("post_setup", hooks.post_setup),
            ("post_argument_parsing", hooks.post_argument_parsing),
        ]


def main(filter_app: Callable[[App], App] = None) -> None:
    with Web3Cli() as app:
        try:
            if filter_app:
                app = filter_app(app)
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except (Web3CliError, Web3CoreError, configparser.NoOptionError) as e:
            print("Web3CliError > %s" % e)
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except (
            web3.exceptions.BadFunctionCallOutput,
            web3.exceptions.BlockNumberOutofRange,
            web3.exceptions.CannotHandleRequest,
            web3.exceptions.InvalidAddress,
            web3.exceptions.NameNotFound,
            web3.exceptions.StaleBlockchain,
            web3.exceptions.MismatchedABI,
            web3.exceptions.ABIEventFunctionNotFound,
            web3.exceptions.ABIFunctionNotFound,
            web3.exceptions.FallbackNotFound,
            web3.exceptions.ValidationError,
            web3.exceptions.ExtraDataLengthError,
            web3.exceptions.NoABIFunctionsFound,
            web3.exceptions.NoABIFound,
            web3.exceptions.NoABIEventsFound,
            web3.exceptions.InsufficientData,
            web3.exceptions.TimeExhausted,
            web3.exceptions.TransactionNotFound,
            web3.exceptions.BlockNotFound,
            web3.exceptions.LogTopicError,
            web3.exceptions.InvalidEventABI,
            web3.exceptions.ContractLogicError,
            web3.exceptions.InvalidTransaction,
            web3.exceptions.TransactionTypeMismatch,
            web3.exceptions.BadResponseFormat,
        ) as e:
            print("web3.py error > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()


def w3eth() -> None:
    """Shorthand command w3eth that uses eth chain"""
    main(lambda a: override_arg(a, "chain", "eth"))


def w3bnb() -> None:
    """Shorthand command that uses bnb chain"""
    main(lambda a: override_arg(a, "chain", "bnb"))


def w3avax() -> None:
    """Shorthand command w3eth that uses avax chain"""
    main(lambda a: override_arg(a, "chain", "avax"))


def w3matic() -> None:
    """Shorthand command w3eth that uses matic chain"""
    main(lambda a: override_arg(a, "chain", "matic"))


def w3cro() -> None:
    """Shorthand command w3eth that uses cro chain"""
    main(lambda a: override_arg(a, "chain", "cro"))


def w3arb() -> None:
    """Shorthand command w3eth that uses arb chain"""
    main(lambda a: override_arg(a, "chain", "arb"))


def w3era() -> None:
    """Shorthand command w3eth that uses zkSync Era chain"""
    main(lambda a: override_arg(a, "chain", "era"))
