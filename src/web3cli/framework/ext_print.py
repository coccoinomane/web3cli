"""
Add the app.print() command to the app object.

app.print() converts the argument to a string and prints
it to screen.

A special case is made for floats and Decimals, which are
printed with a precision of 18 digits.

Why not defining a simple print() function in a module?
Because we want to be able to use last_rendered in tests
to check both the input and the output of app.print.
"""

import decimal
from typing import Any

from cement.core import output
from cement.utils.misc import minimal_logger

from web3cli.framework.app import App

LOG = minimal_logger(__name__)


def extend_print(app: App) -> None:
    def _print(data: Any) -> None:
        app.render(data, handler="print")

    app.extend("print", _print)


class PrintOutputHandler(output.OutputHandler):
    class Meta:
        label = "print"
        overridable = False

    def render(self, data: Any, template: str = None, **kw: Any) -> str:
        LOG.debug("rendering content as text via %s" % self.__module__)
        if type(data) in [float, int, decimal.Decimal]:
            if isinstance(data, int):
                return f"{data}\n"
            else:
                return f"{data:.18g}\n"
        return str(data) + "\n"


def load(app: App) -> None:
    app.handler.register(PrintOutputHandler)
    app.hook.register("pre_argument_parsing", extend_print)
