import json

import requests


def send_tg_message(
    body: str,
    api_key: str,
    chat_id: str,
    disable_notifications: bool = True,
    timeout: int = 1,
) -> bool:
    """
    Send a Telegram message using the REST api.

    Docs: https://core.telegram.org/bots/api#sendmessage
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": chat_id,
        "text": body,
        "parse_mode": "HTML",
        "disable_notification": disable_notifications,
    }

    url = f"https://api.telegram.org/bot{api_key}/sendMessage"

    response = requests.post(
        url, data=json.dumps(data), headers=headers, timeout=timeout
    )

    return response.ok
