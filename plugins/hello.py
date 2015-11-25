"""
# Config (valid YAML document) must be at __doc__.
name: hello     # Name of plugin, lowercase, match with
                # file or package name.
description: "Example plugin for testing bot."
config:                          # Config variable that needed to set
  SHELDON_HELLO_REPLY: 'Hi'      # in environment.
                                 # You must set default values after colon.
"""

import sheldon
import sheldon.utils.logger
import schedule


@sheldon.hooks.message(['hello, bot', 'hey, bot'])
def hello_message(message, bot):
    answer = sheldon.OutgoingMessage(text=bot.config.get('SHELDON_HELLO_REPLY'),
                                     attachments=[])
    bot.send_message(answer)


@sheldon.hooks.command('hello')
def hello_command(message, bot):
    answer = sheldon.OutgoingMessage(text=bot.config.get('SHELDON_HELLO_REPLY'),
                                     attachments=[])
    bot.send_message(answer)


@sheldon.hooks.interval(schedule.every(5).minutes)
def hello_interval(bot):
    sheldon.utils.logger.info_message('Hello from hello module')
