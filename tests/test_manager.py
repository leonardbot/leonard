from leonard import manager, config

bot_config = config.Config()
plugins_manager = manager.PluginsManager(bot_config)


def test_loading_plugins():
    plugins_manager.load_plugins()
    assert plugins_manager.plugins
    for plugin in plugins_manager.plugins:
        assert type(plugin) == manager.Plugin


def test_reloading_plugins():
    plugins = plugins_manager.plugins
    plugins_manager.reload_plugins()
    assert plugins == plugins_manager.plugins


def test_importing_correct_plugin():
    plugin = manager.import_plugin('plugins.hello')
    assert plugin is not None
    # config - python module, so we can check plugin's class
    assert type(plugin) == type(config)


def test_importing_incorrect_plugin():
    plugin  = manager.import_plugin('plugins.hellossssssss')
    assert plugin is None
