from typing import Any
import ruamel.yaml
import os
from web3cli.core.types import Logger


def set(
    filepath: str,
    setting: str,
    value: Any,
    logger: Logger = None,
    section: str = "web3cli",
) -> None:
    """Update a value in the given yaml file. IMPORTANT: use only for
    string settings, non-string settings are not supported yet!

    Source: https://stackoverflow.com/a/49767944/2972183"""

    # Set YAML interface
    yaml = ruamel.yaml.YAML()
    yaml.default_flow_style = False

    # If the config file does not exist, create it
    if not os.path.isfile(filepath):
        with open(filepath, "w") as file:
            config = {section: {setting: value}}
            yaml.dump(config, file)
        if logger:
            logger(f"Created file '{filepath}' with setting '{setting}={value}'")
        return

    # If it exists, load it and update the setting
    with open(filepath, "r") as file:
        config = yaml.load(file)
        config[section][setting] = value

    # Dump the modified config to file
    with open(filepath, "w") as file:
        yaml.dump(config, file)

    if logger:
        logger(f"Updated file '{filepath}' with setting '{setting}={value}'")
