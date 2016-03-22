"""
name: stackoverflow
description: "Search questions on Stackoverflow"
priority: 250
"""
import json
import requests
import leonard
import leonard.utils

STACKOVERFLOW_API = 'https://api.stackexchange.com/2.2/search?order=desc&pagesize=3&sort=activity&intitle={}&site={}&key={}'
STACKOVERFLOW_SEARCH = 'http://stackoverflow.com/search?q={}'


@leonard.hooks.start_end(['stackoverflow', 'sof', 'overflow', 'хэшкод'])
def search_question(message, bot):
    query = message.variables['query']
    if not query:
        raise leonard.utils.NextHook

    questions_data = message.locale.search_questions(query, bot)
    if not questions_data:
        answer = leonard.OutgoingMessage(
            recipient=message.sender,
            text=message.locale.not_found.format(query)
        )
        bot.send_message(answer)
        raise leonard.utils.NextHook

    answer_text = message.locale.found.format(query)
    for question in questions_data:
        answer_text += '{} - {}\n\n'.format(question['title'], question['link'])
    answer_text += message.locale.more_in.format(query)

    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=answer_text,
        variables={"telegram_hide_preview": True}
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'

    not_found = "Sorry, but I've not found '{}' on Stackoverflow"

    found = "So I have found in Stackoverflow by '{}' query this questions:\n\n"

    more_in = 'More in ' + STACKOVERFLOW_SEARCH

    def search_questions(self, query, bot):
        response = requests.get(
            STACKOVERFLOW_API.format(query, 'stackoverflow',
                                     bot.config.get('LEONARD_STACKOVERFLOW_TOKEN'))
        )
        data = json.loads(response.text)
        return data['items']


class RussianLocale:
    language_code = 'ru'

    not_found = "Извини, я не нашел '{}' на Stackoverflow"

    found = "Я нашел на Stackoverflow по запросу '{}' эти вопросы:\n\n"

    more_in = "Больше на " + STACKOVERFLOW_SEARCH

    def search_questions(self, query, bot):
        response = requests.get(
            STACKOVERFLOW_API.format(query, 'ru.stackoverflow',
                                     bot.config.get('LEONARD_STACKOVERFLOW_TOKEN'))
        )
        data = json.loads(response.text)
        return data['items']
