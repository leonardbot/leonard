"""
# ADAPTER CURRENTLY NOT WORKING. USE TELEGERAM ADAPTER.
# Config (valid YAML document) must be at __doc__.
name: console # Name of adapter, lowercase, match with
              # file or package name.
description: "Example adapter for testing bot."
config:                          # Config variable that needed to set
  LEONARD_EXAMPLE_VARIABLE: 'aa' # in environment.
                                 # You can set default values after colon.
"""
from os import getlogin
from time import sleep
from random import randint
from leonard.adapter import IncomingMessage, Attachment

# Code running on adapter loading may be here


def get_messages(bot):
    variables = {
        'first_name': input('Your first name: '),
        'last_name': input('Your last name: '),
        'adapter': 'console'
    }
    while True:
        # Let plugin thread end
        sleep(1)
        text = input('Enter message: ')
        location_text = input('Enter location (if no, just leave it blank):')
        location = None
        if location_text:
            location = tuple(map(float, location_text.split()))
        variables['last_message'] = {'text': text, 'from': {'id': 1}}
        variables['location'] = location
        yield IncomingMessage(
            adapter_id='console1',
            text=text,
            attachments=[],
            location=location,
            variables=variables
        )
    return []


def send_message(message, bot):
    print('BOT: ', message.text)
    print(message.recipient.data)
    print('Attachments:')
    for attachment in message.attachments:
        print(attachment.id)
        print(attachment.type)
        print(attachment.path)
        print(attachment.text)
