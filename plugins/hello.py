"""
# Config (valid YAML document) must be at __doc__.
name: hello     # Name of plugin, lowercase, match with
                # file or package name.
description: "Example plugin for testing bot."
priority: 1
config:                            # Config variable that needed to set
  LEONARD_SOME_API_KEY: '123'      # in environment.
                                   # You must set default values after colon.
"""

import leonard
import schedule


@leonard.hooks.message(['hello, bot', 'hey, bot'])
def hello_message(message, bot):
    answer = leonard.OutgoingMessage(
        text=leonard.get_text('hello.hello_message', message),
        attachments=[]
    )
    bot.send_message(answer)


@leonard.hooks.command('hello')
def hello_command(message, bot):
    answer = leonard.OutgoingMessage(
        text=leonard.get_text('hello.hello_message', message),
        attachments=[]
    )
    bot.send_message(answer)


@leonard.hooks.interval(schedule.every(5).minutes)
def hello_interval(bot):
    leonard.logger.info_message('Hello from hello module')
