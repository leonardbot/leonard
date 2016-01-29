from leonard import storage, Leonard

# Create bot
bot = Leonard({'config-prefix': 'LEONARD_',
               'adapter': 'console'})


def test_storage_existing():
    assert bot.storage.redis is not None


def test_setting_value():
    result = bot.storage.set('test_key', 'test_value')
    assert result is not None

    result = bot.storage.get('test_key').decode()
    assert result == 'test_value'


def test_default_value():
    # Default default value
    result = bot.storage.get('test_non_existing_key')
    assert result is None

    # Custom default value
    result = bot.storage.get('test_non_existing_key', 0)
    assert result == 0
