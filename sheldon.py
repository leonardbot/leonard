import re
import os


class Sheldon:
    loaded_modules = []

    def __init__(self, bot_language, bot_adapter):
        self.language = bot_language
        self.adapter = bot_adapter

    def load_modules(self):
        python_file_regexp = re.compile("(.+)\.py")
        modules_folder = os.listdir('modules')
        for file in modules_folder:
            regexp_match = python_file_regexp.match(file)
            if regexp_match is not None:
                module_name = regexp_match.group(1)
                try:
                    module = __import__('modules.' + module_name,
                                        fromlist=[''])
                except ImportError as error_msg:
                    print(error_msg)
                    print("Error with importing module", module_name)
                    continue

                self.loaded_modules.append({
                    "name": module_name,
                    "module": module,
                    "config": module.module_config
                })

        if not self.loaded_modules:
            print("No one module loaded.")

