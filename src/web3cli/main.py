from cement import App, init_defaults
from cement.core.exc import CaughtSignal
from web3cli.controllers.base_controller import BaseController
from web3cli.controllers.chain_controller import ChainController
from web3cli.controllers.rpc_controller import RpcController
from web3cli.controllers.address_controller import AddressController
from web3cli.controllers.signer_controller import SignerController
from web3cli.controllers.config_controller import ConfigController
from web3cli.controllers.key_controller import KeyController
from web3cli.controllers.tx_controller import TxController
from web3cli.core.exceptions import Web3CliError
from web3cli import hooks
import os

# Configuration defaults
CONFIG = init_defaults("web3cli")
CONFIG["web3cli"] = {
    "app_key": None,
    "debug": False,
    "default_chain": "ethereum",
    "default_signer": None,
    "default_priority_fee": 1,
    "db_file": os.path.join(
        os.path.expanduser("~"), ".web3cli", "database", "web3cli.sqlite"
    ),
    "output_table_format": "fancy_grid",
    "output_table_wrap": 33,
}

# Allow to use `w3 -o json` for json output
META = init_defaults("output.json")
META["output.json"]["overridable"] = True


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

        ### override default handler meta options
        meta_defaults = META

        # register handlers
        handlers = [
            BaseController,
            ChainController,
            RpcController,
            SignerController,
            AddressController,
            ConfigController,
            KeyController,
            TxController,
        ]

        # extend the app with cement hook system
        hooks = [
            ("post_setup", hooks.post_setup),
            ("post_argument_parsing", hooks.post_argument_parsing),
        ]


def main() -> None:
    with Web3Cli() as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except Web3CliError as e:
            print("Web3CliError > %s" % e.args[0])
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
