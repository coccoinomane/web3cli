import json
from typing import Any, List

from web3 import Web3

from web3cli.framework.app import App
from web3core.helpers.format import wrap as wrap_


def render_table(
    app: App, headers: List[str], data: List[List[Any]], wrap: int = None
) -> None:
    """Print data as a table"""
    app.render(
        [[prepare_for_table(app, value, wrap) for value in row] for row in data],
        headers=headers,
        handler="tabulate",
    )


def prepare_for_table(app: App, value: Any, wrap: int = None) -> str:
    """Prepare a value before it is printed in a table"""
    # Parse wrap parameter
    if wrap == None:
        wrap = app.get_option("output_table_wrap")
    elif wrap == 0:
        wrap = 100000
    # Wrap value
    try:
        return "\n".join(wrap_(s=value, n=wrap))
    except:
        return value


def render_json(app: App, data: Any, indent: int = 4) -> None:
    """Print data as a JSON"""
    app.render(data, handler="json", indent=indent)
    print()


def render_yaml(app: App, data: Any) -> None:
    """Print data as a YAML"""
    app.render(data, handler="yaml")


def render_web3py(app: App, data: Any, indent: int = 4) -> None:
    """Print AttributeDicts from Web3.py as a json"""
    render_json(app, json.loads(Web3.to_json(data)), indent=indent)


def render(app: App, data: Any) -> None:
    """Print the given variable to screen.

    Dictionaries, lists and web3py AttributeDicts are printed as
    JSON.

    All the rest is converted to string by app.print() and printed
    to screen (see ext_print.py)"""
    if type(data).__name__ == "AttributeDict":
        render_web3py(app, data)
    elif type(data) in [dict, list]:
        render_json(app, data)
    elif type(data) in [set]:
        render_json(app, list(data))
    else:  # strings, booleans and everything else
        app.print(data)
