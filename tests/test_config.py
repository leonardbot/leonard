from leonard import config, adapter


def test_creating_adapter():
    result = config.Config()
    assert result is not None
    assert result.variables is not None
    assert type(result.variables) == dict


def test_installed_plugins_list():
    result = config.Config()
    with open('installed_plugins.txt') as file:
        file_data = file.read()
        plugins = file_data.split('\n')
    assert plugins == result.installed_plugins


def test_parsing_adapter_config():
    test_adapter = adapter.load_adapter('console')
    result = config.parse_config(test_adapter.module, 'adapter')
    assert result is not None
    assert result.name == test_adapter.name
    assert type(result.variables) == dict
