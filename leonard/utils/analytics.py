import json
import requests

BOTAN_URL = 'https://api.botan.io/track?token={token}&uid={uid}&name={name}'


def track_message(message, adapter, plugin, bot):
    """
    Track message in Botan.io

    :param message: dict, message from telegram
    :param adapter: str, adapter name
    :param plugin: str, name of plugin that proceed that message
    :param bot: Leonard object
    """
    message['adapter'] = adapter
    url = BOTAN_URL.format(token=bot.config.get('LEONARD_BOTAN_TOKEN'),
                           uid=message['from']['id'], name=plugin)
    try:
        response = requests.post(
            url, data=json.dumps(message),
            headers={'Content-type': 'application/json'}
        )
        return response
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        return None
