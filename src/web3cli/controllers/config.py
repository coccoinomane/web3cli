from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers import yaml


class Config(Controller):
    """Handler of the `web3 config` commands"""

    class Meta:
        label = "config"
        help = "show, add or edit web3cli's setting values"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="show the value of the given setting. If no setting is given, show all settings",
        arguments=[
            (
                ["setting"],
                {
                    "help": "setting to inspect, for example 'default_network'",
                    "nargs": "?",
                    "action": "store",
                },
            ),
        ],
    )
    def get(self) -> None:
        pass
        if self.app.pargs.setting:
            self.app.print(self.app.config.get("web3cli", self.app.pargs.setting))
        else:
            output = {}
            all_config = self.app.config.get_dict()
            for section in ["web3cli", "web3cli_test"]:
                output[section] = all_config[section]
            self.app.render(output, handler="yaml")

    @ex(
        help="set the value of a setting; by default it writes to the local configuration file (web3cli.yml). IMPORTANT: supports only string settings!",
        arguments=[
            (
                ["setting"],
                {
                    "help": "setting to set, for example 'default_network'",
                    "action": "store",
                },
            ),
            (
                ["value"],
                {
                    "help": "value for the setting, for example 'ethereum'",
                    "action": "store",
                },
            ),
            (
                ["-g", "--global"],
                {
                    "help": "save to the configuration file in your home folder ( $HOME/.web3cli/config/web3cli.yml)",
                    "dest": "is_global",
                    "action": "store_const",
                    "const": True,
                },
            ),
        ],
    )
    def set(self) -> None:
        filepath = (
            self.app.Meta.config_files[0]
            if self.app.pargs.is_global
            else self.app.Meta.config_files[-1]
        )

        yaml.set(
            filepath=filepath,
            setting=self.app.pargs.setting,
            value=self.app.pargs.value,
            logger=self.app.log,
            section="web3cli",
        )

    @ex(help="show the location of the configuration files")
    def where(self) -> None:
        self.app.print("\n".join(self.app.Meta.config_files))
