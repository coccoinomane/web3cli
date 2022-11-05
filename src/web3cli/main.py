from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from web3cli.controllers.network import Network
from web3cli.controllers.address import Address
from web3cli.core.exceptions import Web3CliError
from web3cli.controllers.base import Base
from web3cli.helpers import database

# configuration defaults
CONFIG = init_defaults("web3cli", "web3cli_test")
CONFIG["web3cli"]["debug"] = False
CONFIG["web3cli"]["default_network"] = "ethereum"
CONFIG["web3cli"]["db_file"] = "~/.web3cli/database/web3cli.sqlite"
CONFIG["web3cli_test"]["db_file"] = "~/.web3cli/database/web3cli_test.sqlite"


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

        # Path of configuration file(s)
        config_files = ["config/web3cli.yml", "~/.web3cli/config/web3cli.yml"]

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "jinja2"

        # register handlers
        handlers = [Base, Network, Address]

        #
        hooks = [
            ("post_setup", database.attach_production_db),
        ]


class Web3CliTest(TestApp, Web3Cli):
    """A sub-class of Web3Cli that is better suited for testing."""

    class Meta:
        label = "web3cli"

        hooks = [
            ("post_setup", database.attach_testing_db),
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
