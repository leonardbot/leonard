"""
# Config (valid YAML document) must be at __doc__.
name: hello     # Name of plugin, lowercase, match with
                # file or package name.
description: "Example plugin for testing bot."
config:                          # Config variable that needed to set
  SHELDON_HELLO_REPLY: 'Hi'      # in environment.
                                 # You must set default values after colon.
"""

import leonard
import leonard.utils.logger
import schedule


@leonard.hooks.message(['hello, bot', 'hey, bot'])
def hello_message(message, bot):
    answer = leonard.OutgoingMessage(text=bot.config.get('SHELDON_HELLO_REPLY'),
                                     attachments=[])
    bot.send_message(answer)


@leonard.hooks.command('hello')
def hello_command(message, bot):
    answer = leonard.OutgoingMessage(text=bot.config.get('SHELDON_HELLO_REPLY'),
                                     attachments=[])
    bot.send_message(answer)


@leonard.hooks.interval(schedule.every(5).minutes)
def hello_interval(bot):
    leonard.utils.logger.info_message('Hello from hello module')
