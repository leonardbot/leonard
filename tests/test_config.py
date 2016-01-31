from leonard import config, adapter


def test_creating_adapter():
    result = config.Config()
    assert result is not None
    assert result.variables is not None
    assert type(result.variables) == dict


def test_installed_plugins_list():
    result = config.Config()
    assert 'plugins.hello' in result.installed_plugins
    assert 'plugins.registration' in result.installed_plugins
    assert 'plugins.__pycache__' not in result.installed_plugins
    for plugin in result.installed_plugins:
        # result.installed_plugins containts full import paths,
        # like "plugins.hello". To get plugin name,
        # we need to split "plugins.hello" to ['plugins', 'hello']
        # and get second (first from zero) element
        plugin_name = plugin.split('.')[1]
        assert not plugin_name.startswith('.')
        assert not plugin_name.startswith('__')


def test_parsing_adapter_config():
    test_adapter = adapter.load_adapter('console')
    result = config.parse_config(test_adapter.module, 'adapter')
    assert result is not None
    assert result.name == test_adapter.name
    assert type(result.variables) == dict
