from typing import Any, List

from cement import App

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
        wrap = app.config.get("web3cli", "output_table_wrap")
    elif wrap == 0:
        wrap = 100000
    # Wrap value
    try:
        return "\n".join(wrap_(s=value, n=wrap))
    except:
        return value
