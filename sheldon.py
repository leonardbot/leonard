import re
import os


class Sheldon:
    """
    Sheldon class - main class of the bot.
    When bot starting, creating new instance of Sheldon.
    """
    loaded_modules = {}
    loaded_adapter = {}

    def __init__(self, language, adapter_name):
        """
        Constructor, which creating new bot and loading adapter.

        :param language: string, 'en' or 'ru'
        :param adapter_name: string, for example, 'console'
        :return:
        """
        self.language = language
        self.adapter_name = adapter_name
        self.adapter = self.load_adapter(adapter_name)
        self.blocked_users = self.adapter.adapter_config['blocked_users_id']
        self.admins = self.adapter.adapter_config['admin_ids']

    def add_module(self, module_name):
        """
        Adding new module to connected modules

        :param module_name: string, for example, 'test' or 'say'
        :return: bool, if everything ok - True, else - False
        """
        try:
            module = __import__('modules.' + module_name,
                                fromlist=[''])
        except ImportError as error_msg:
            print(error_msg)
            print("Error with importing module", module_name)
            return False

        # If in config specificated some adapters,
        # check, can this adapter work with this module
        if module.module_config['adapters']:
            if self.adapter_name not in module.module_config['adapters']:
                return False

        module_regexps = []
        for regexp in module.module_config['regexps'][self.language]:
            module_regexps.append(re.compile(regexp, re.IGNORECASE))

        self.loaded_modules.update({
            module_name: {
                "module": module,
                "config": module.module_config,
                "regexps": module_regexps
            }
        })
        return True

    def delete_module(self, module_name):
        """
        Delete module from connected modules

        :param module_name: string, for example, 'test' or 'say'
        :return:
        """
        try:
            self.loaded_modules.pop(module_name)
            return True
        except KeyError:
            print("Module {} is not loaded".format(module_name))
            return False

    def load_modules(self):
        """
        Function for load all modules from modules folder

        :return:
        """
        python_file_regexp = re.compile("(.+)\.py")
        modules_folder = os.listdir('modules')
        for file in modules_folder:
            regexp_match = python_file_regexp.match(file)
            if regexp_match is not None:
                module_name = regexp_match.group(1)
                self.add_module(module_name)

        if not self.loaded_modules:
            print("No one module loaded.")
        else:
            print("Loaded {} modules".format(str(len(self.loaded_modules))))

    def load_adapter(self, adapter_name='console'):
        """
        Load adapter for bot

        :param adapter_name: string, for example, 'console'
        :return:
        """
        try:
            adapter = __import__('adapters.' + adapter_name,
                                 fromlist=[''])
        except ImportError as error_msg:
            adapter = None
            print(error_msg)
            print("Fatal: Error when connecting with adapter")
            exit()
        print("Loaded adapter", adapter_name)
        return adapter

    def get_messages(self):
        """
        Function to check and get new messages from adapter

        :return: list of dictionaries, with 'text', 'time',
                 'sender_id', 'sender_name', 'sender_type'
        """
        new_messages = self.adapter.get_messages()
        return new_messages

    def parse_message(self, message):
        """
        Function to search modules which matching with message
        and send message to that module

        :param message: incoming message
        :return:
        """
        for module in self.loaded_modules:
            for regexp in self.loaded_modules[module]['regexps']:
                message_match = regexp.match(message['text'])
                if message_match is not None:
                    if message['user_id'] not in self.blocked_users:
                        self.loaded_modules[module]['module'].get_answer(
                            message=message,
                            lang=self.language,
                            bot=self,
                            options=message_match.groups()
                        )
                    return True
        # If message not matching with any modules,
        # but message starts from '!', send message
        # that command is bad.
        if message['text']:
            if message['text'][0] == '!':
                if self.language == 'en':
                    problem_message = 'Command is bad. Check it again.'
                elif self.language == 'ru':
                    problem_message = 'Команда не распознана. ' + \
                                      'Проверьте ее еще раз.'
                else:
                    print('Choose correct bot language')
                    return False

                self.send_message(message['sender_id'], message['sender_type'],
                                  message_text=problem_message)

    def send_message(self, sender_id, sender_type,
                     message_text='', message_photos=[]):
        adapter_response = self.adapter.send_message(
            sender_id, sender_type,
            message_text, message_photos
        )
        if adapter_response:
            return True
        else:
            print("Error with sending message '{}'".format(message_text))
            return False

    def is_admin(self, user_id):
        """Function, that checks is user admin of adapter or not"""
        if user_id in self.admins:
            return True
        else:
            return False


class SheldonTest(Sheldon):
    """
    Class for unit-tests of modules.
    Some functions (like send_message) are rewrote specialy
    for testing modules
    """
    def __init__(self, language):
        super().__init__(language, 'console')
        self.sent_messages = []

    def send_message(self, sender_id, sender_type,
                     message_text='', message_photos=[]):
        self.sent_messages.append(
            {
                'sender_id': sender_id,
                'sender_type': sender_type,
                'message_text': message_text,
                'message_photos': message_photos
            }
        )