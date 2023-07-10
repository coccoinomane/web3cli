from cement import ex

from web3cli.framework.controller import Controller
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
        arguments=[
            (["--message"], {"default": "Hello world 🤗"}),
            (["--chat"], {"action": "store"}),
        ],
    )
    def telegram(self) -> None:
        chat_id = self.app.pargs.chat or self.app.get_option("telegram_chat_id")
        if send_tg_message(self.app, self.app.pargs.message, chat_id):
            render(self.app, "Ok ✅")
        else:
            render(self.app, "Error ❌")
