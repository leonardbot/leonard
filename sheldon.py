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

        self.loaded_modules.update({
            module_name: {
                "module": module,
                "config": module.module_config
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



