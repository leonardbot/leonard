"""
name: gif
description: Gif search based (or random gif) on Giphy API
priority: 300
"""
import json
import requests
import leonard
import leonard.utils
import leonard.utils.ru

GIPHY_BASE = 'http://api.giphy.com/v1/gifs/'
GIPHY_RANDOM = GIPHY_BASE + 'random?api_key={}'
GIPHY_SEARCH = GIPHY_BASE + 'translate?s={}&api_key={}'
GIF_RU_WORDS = (leonard.utils.ru.vowel_ends('гифк') +
                leonard.utils.ru.vowel_ends('гиф'))


def random_gif(bot):
    response = requests.get(
        GIPHY_RANDOM.format(bot.config.get('LEONARD_GIPHY_TOKEN'))
    )
    gif_url = json.loads(response.text)['data']['image_url']
    return leonard.utils.download_file(gif_url, 'gif')


def search_gif(query, bot):
    response = requests.get(GIPHY_SEARCH.format(
        query, bot.config.get('LEONARD_GIPHY_TOKEN'))
    )
    return json.loads(response.text)['data']


@leonard.hooks.start_end(GIF_RU_WORDS + ['gif'])
def send_gif(message, bot):
    query = message.variables['query']
    if not query:
        gif_attachment = leonard.Attachment('document', random_gif(bot))
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.random_gif,
            attachments=[gif_attachment]
        )
        bot.send_message(answer)
        return
    gif = search_gif(query, bot)
    if not gif:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.not_found.format(query)
        )
        bot.send_message(answer)
        return
    gif_path = leonard.utils.download_file(gif['images']['original']['url'], 'gif')
    gif_attachment = leonard.Attachment('document', gif_path)
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.your_gif.format(query),
        attachments=[gif_attachment]
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'

    random_gif = 'Your random gif'

    not_found = "I haven't found any gifs for '{}' query"

    your_gif = "Your '{}' gif"


class RussianLocale:
    language_code = 'ru'

    random_gif = 'Твоя случайная гифка'

    not_found = "Я не нашел никаких гифок по запросу '{}'"

    your_gif = 'Твоя гифка по запросу "{}"'
