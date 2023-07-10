from typing import Any

import web3core.helpers.telegram
from web3cli.exceptions import Web3CliError
from web3cli.framework.app import App


def send_tg_message(
    app: App, body: str, chat_id: str = None, silent: bool = False, **kwargs: Any
) -> bool:
    """
    Send a telegram message to the given chat ID.

    Parameters
    ----------
    body : str
        The message to send; it can include emojis.
    chat_id : str
        The recipient chat or user.  If not provided, it will be read from the config.
    silent : bool
        Send a silent, so that it doesn't make the phone vibrate or make a sound.
    """

    api_key = app.get_option("telegram_api_key")
    chat_id = chat_id or app.get_option("telegram_chat_id")
    timeout = int(app.get_option("telegram_send_timeout")) or 5

    if not api_key or not chat_id:
        raise Web3CliError(
            "Please set your Telegram API key and chat ID using `w3 config set telegram_api_key <api_key>` and `w3 config set telegram_chat_id <chat_id>``"
        )

    notification_result = False

    try:
        notification_result = web3core.helpers.telegram.send_tg_message(
            body=body,
            api_key=api_key,
            chat_id=chat_id,
            timeout=timeout,
            disable_notifications=silent,
            **kwargs,
        )
    except Exception as e:
        app.log.error(f"Failed to send Telegram notification: {e}")
        return False

    return notification_result
