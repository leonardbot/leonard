import re
import os
import settings


class Sheldon:
    language = settings.bot_language
    adapter = settings.bot_adapter

    loaded_modules = []

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

