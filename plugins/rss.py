"""
name: rss
description: get last news from rss channels
priority: 400
"""

import feedparser
import leonard
from plugins.news import get_news_data

MEDIA_LIST = [(('buzzfeed', 'bf'), 'http://www.buzzfeed.com/index.xml'),
              (('re/code', 'recode', 'r/c'), 'http://recode.net/feed/'),
              (('tnw', 'the next web', 'thenextweb'), 'http://feeds2.feedburner.com/thenextweb'),
              (('vc', 'vc.ru', 'цукерберг позвонит'), 'https://vc.ru/feed'),
              (('tj', 'tjournal', 'тж'), 'https://tjournal.ru/rss')]


@leonard.hooks.callback(
    lambda message, bot: any(map(lambda x: message.text in x[0], MEDIA_LIST))
)
def last_news_message(message, bot):
    for media in MEDIA_LIST:
        if message.text in media[0]:
            rss_link = media[1]
    news_data = get_news_data(rss_link, 3)
    articles = []
    for article in news_data:
        articles.append(message.locale.article.format(article['title'],
                                                      article['url']))
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text='\n\n'.join(articles)
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'
    article = '{} - {}'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'
    article = '{} - {}'
