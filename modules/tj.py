import feedparser
import requests
from pyquery import PyQuery
from time import sleep


module_config = {
    "name": "tj",
    "public_name": {
        "en": "TJ",
        "ru": "TJ"
    },
    "description": {
        "en": "Show last news, best tweets and media analyze from TJ",
        "ru": "Показать последние новости, анализ медиа и лучшие твиты из TJ"
    },
    "regexps": {
            "en": [
                "!tj(ournal)?"
            ],
            "ru": [
                "!tj(ournal)?",
                "!тж(урнал)?"
            ]
    },
    "command_format": {
        "en": "!tj",
        "ru": "!tj"
    },
    "examples": {
        "en": [
            "!tj"
        ],
        "ru": [
            "!tj"
        ]
    },
    "adapters": []
}


def get_3_latest_news():
    latest_news = ['Последние новости:']
    news = feedparser.parse('http://tjournal.ru/rss')['items']
    # Get 3 news
    for i in range(3):
        latest_news.append('{title} - {link}'.format(
            title=news[i]['title'],
            link=news[i]['link']
        ))
    return latest_news


def get_media_analyze(press_type):
    media_news = ['Анализ СМИ:']
    get_block_query = '.container .b-content .b-block #blockNews{}'
    get_article_query = '.b-index-news .b-index-news__b:eq( {} )'
    # Select num, which contains in DOM.
    # For example, "#blockNews2" is the
    # block with russian news
    if press_type == 'russian':
        press_num = 2
    elif press_type == 'russian_it':
        press_num = 1
    elif press_type == 'english_it':
        press_num = 3
    elif press_type == 'ukrainian':
        press_num = 5
    elif press_type == 'belarusian':
        press_num = 7
    else:
        print('Unsupporting press type')
        return []
    news_html = PyQuery(requests.get('http://tjournal.ru/news').text)
    news_block_html = news_html(get_block_query.format(str(press_num)))
    # Get 3 articles
    for i in range(3):
        article_html = news_block_html(get_article_query.format(str(i)))
        # Article title contains in the link with tag <b>
        article_title = article_html('a b').text()
        # Article source contains in 'alt' attribute of image
        article_source = article_html('a img').attr('alt')
        article_link = article_html('a').attr('href')
        media_news.append('{source}: {title} - {link}'.format(
            source=article_source,
            title=article_title,
            link=article_link
        ))
    return media_news


def get_3_best_tweets():
    best_tweets = ['Лучшие твиты:']
    # HTML query in jQuery style to get best tweets
    html_query = '.container .b-content .b-content-wrapper ' + \
                 '.b-content__b1 .b-block .b-articles ' + \
                 '.b-articles__b'
    tj_tweets_page = requests.get('http://tjournal.ru/tweets').text
    tweets_html = PyQuery(tj_tweets_page)
    # Get 3 tweets
    for i in range(3):
        html_tweet_query = html_query + ':eq( {} )'.format(str(i))
        tweet_html = tweets_html(html_tweet_query)
        tweet_text = tweet_html('.b-articles__b__text').text()
        tweet_author = tweet_html('.b-articles__b__name').text()
        best_tweets.append('{author}: "{tweet}"'.format(
            author=tweet_author,
            tweet=tweet_text
        ))
    return best_tweets


def get_answer(message, lang, bot, options):
    digest = get_3_latest_news() + get_3_best_tweets() + \
             get_media_analyze('russian')
    for send_message in digest:
        bot.send_message(
            message_text=send_message,
            sender_id=message['sender_id'],
            sender_type=message['sender_type']
        )
        sleep(1)
    return True