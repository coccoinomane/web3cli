import argparse

from cement import ex

from web3cli.framework.controller import Controller
from web3cli.helpers.config import update_setting_in_config_file
from web3cli.helpers.render import render, render_yaml


class ConfigController(Controller):
    """Handler of the `w3 config` commands"""

    class Meta:
        label = "config"
        help = "Manage the app settings"
        stacked_type = "nested"
        stacked_on = "base"
        aliases = ["option"]

    @ex(
        help="show the value of the given setting. If no setting is given, show all settings",
        arguments=[
            (
                ["setting"],
                {
                    "help": "setting to inspect, for example 'default_chain'",
                    "nargs": "?",
                },
            ),
        ],
    )
    def get(self) -> None:
        if self.app.pargs.setting:
            render(self.app, self.app.get_option(self.app.pargs.setting))
        else:
            output = {}
            all_config = self.app.config.get_dict()
            for section in [self.app._meta.config_section]:
                output[section] = all_config[section]
            render_yaml(self.app, output)

    @ex(
        help="set the value of a setting. IMPORTANT: supports only string settings!",
        arguments=[
            (
                ["setting"],
                {
                    "help": "setting to set, for example 'default_chain'",
                },
            ),
            (
                ["value"],
                {
                    "help": "value for the setting, for example 'eth'",
                },
            ),
            (
                ["-g", "--global"],
                {
                    "help": "whether to save the setting globally (default) or locally",
                    "dest": "is_global",
                    "action": argparse.BooleanOptionalAction,
                    "default": True,
                },
            ),
        ],
    )
    def set(self) -> None:
        update_setting_in_config_file(
            self.app,
            setting=self.app.pargs.setting,
            value=self.app.pargs.value,
            do_log=True,
            is_global=self.app.pargs.is_global,
        )

    @ex(help="show the location of the configuration files")
    def where(self) -> None:
        render(self.app, "\n".join(self.app.Meta.config_files))
