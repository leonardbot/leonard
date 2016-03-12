"""
name: utils
description: reusable bot messages, like cancel from question
priority: 100
"""

import leonard
import time


def cancel_from_question(message, bot):
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=bot.get_locale(
            'utils', message.sender.data.get('language', 'en')
        ).cancel_from_question
    )
    bot.send_message(answer)


class EnglishLocale:
    language_code = 'en'
    cancel_from_question = 'Fine.'
    question_explanation = ("You can answer question in 1 hour - "
                            "or I will forget about it.\n"
                            "If you don't want to answer - just send 'Oops' "
                            "and consider it gone.")

    def format_datetime(self, timestamp, utc_offset=0):
        local_time = time.gmtime(timestamp + utc_offset)
        return time.strftime('%B %d, %Y. %H:%M', local_time)


class RussianLocale:
    language_code = 'ru'
    cancel_from_question = 'Ладно.'
    question_explanation =  ('Ты можешь ответить на вопрос в течение часа, '
                             'потому что потом я могу забыть о нем.\n'
                             'Если не хочешь отвечать, отправь "Ой" и '
                             'будем считать, что ничего не было.')
    months = {
        1: ('Январь', 'Января'), 2: ('Февраль', 'Февраля'),
        3: ('Март', 'Марта'), 4: ('Апрель', 'Апреля'),
        5: ('Май', 'Мая'), 6: ('Июнь', 'Июня'),
        7: ('Июль', 'Июль'), 8: ('Август', 'Августа'),
        9: ('Сентябрь', 'Сентября'), 10: ('Октябрь', 'Октября'),
        11: ('Ноябрь', 'Ноября'), 12: ('Декабря', 'Декабря')
    }

    def format_datetime(self, timestamp, utc_offset=0):
        local_time = time.gmtime(timestamp + utc_offset)
        for (month_num, month_names) in self.months.items():
            if month_num == local_time.tm_mon:
                month_name = month_names[1]
        return "{day} {month} {year} г., {hour}:{minutes}".format(
            day=local_time.tm_mday, month=month_name.lower(),
            year=local_time.tm_year, hour=local_time.tm_hour,
            minutes=local_time.tm_min
        )
