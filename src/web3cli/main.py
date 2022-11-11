from cement import App, init_defaults
from cement.core.exc import CaughtSignal
from web3cli.controllers.network import Network
from web3cli.controllers.address import Address
from web3cli.controllers.signer import Signer
from web3cli.controllers.config import Config
from web3cli.controllers.key import Key
from web3cli.core.exceptions import Web3CliError
from web3cli.controllers.base import Base
from web3cli import hooks
import os

# configuration defaults
CONFIG = init_defaults("web3cli")
CONFIG["web3cli"]["app_key"] = None
CONFIG["web3cli"]["debug"] = False
CONFIG["web3cli"]["default_network"] = "ethereum"
CONFIG["web3cli"]["default_signer"] = None
CONFIG["web3cli"]["db_file"] = os.path.join(
    os.path.expanduser("~"), ".web3cli", "database", "web3cli.sqlite"
)


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
        output_handler = "jinja2"

        # register handlers
        handlers = [Base, Network, Signer, Address, Config, Key]

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
