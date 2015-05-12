import re
import os


class Sheldon:
    loaded_modules = {}
    loaded_adapter = {}

    def __init__(self, language, adapter_name):
        self.language = language
        self.adapter = self.load_adapter(adapter_name)

    def add_module(self, module_name):
        try:
            module = __import__('modules.' + module_name,
                                fromlist=[''])
        except ImportError as error_msg:
            print(error_msg)
            print("Error with importing module", module_name)
            return False

        module_regexps = []
        for regexp in module.module_config['regexps'][self.language]:
            module_regexps.append(re.compile(regexp))


        self.loaded_modules.update({
            module_name: {
                "module": module,
                "config": module.module_config,
                "regexps": module_regexps
            }
        })
        return True

    def delete_module(self, module_name):
        try:
            self.loaded_modules.pop(module_name)
        except KeyError:
            print("Module {} is not loaded".format(module_name))

    def load_modules(self):
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

    def reload_modules(self):
        self.loaded_modules = {}
        self.load_modules()

    def load_adapter(self, adapter_name='console'):
        try:
            adapter = __import__('adapters.' + adapter_name,
                                 fromlist=[''])
        except ImportError as error_msg:
            adapter = None
            print(error_msg)
            print("Fatal: Error when connecting with adapter")
            exit()
        return adapter

    def get_messages(self):
        new_messages = self.adapter.get_messages()
        return new_messages

    def parse_message(self, message):
        for module in self.loaded_modules:
            for regexp in self.loaded_modules[module]['regexps']:
                message_match = regexp.match(message['text'])
                if message_match is not None:
                    self.loaded_modules[module]['module'].get_answer(
                        message=message,
                        lang=self.language,
                        bot=self
                    )
                    return True

    def send_message(self, message_text,
                     message_photos=[], options={}):
        adapter_response = self.adapter.send_message(
            message_text, message_photos, options
        )
        if adapter_response:
            return True
        else:
            print("Error with sending message '{}'".format(message_text))
            return False



