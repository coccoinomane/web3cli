from cement import ex

from web3cli.controllers.controller import Controller
from web3cli.helpers.render import render
from web3cli.helpers.telegram import send_tg_message


class DebugController(Controller):
    """Handler for commands used for debugging purposes"""

    class Meta:
        label = "debug"
        help = "Commands used for debugging purposes"
        stacked_type = "nested"
        stacked_on = "base"
        hide = True

    @ex(
        help="Send a Telegram message to the configured chat.  Useful for testing notifications.",
        arguments=[(["--message"], {"default": "Hello world 🤗"})],
    )
    def telegram(self) -> None:
        if send_tg_message(self.app, self.app.pargs.message):
            render(self.app, "Ok ✅")
        else:
            render(self.app, "Error ❌")
