import time
from leonard import db, Leonard

# Create bot
bot = Leonard({'config-prefix': 'LEONARD_',
               'adapter': 'console'})
# Connect to database
database = db.Database(bot, 'LEONARD_')

def test_db_creation():
    assert database is not None


def test_finding_user_by_adapter_id():
    # time.time() - test adapter_id
    adapter_id = time.time()
    database.create_new_user(adapter_id)
    result = database.find_by_adapter_id(adapter_id)
    assert result is not None
    assert result.adapter_id == adapter_id


def test_creating_user_by_find():
    # Unexisting adapter_id
    adapter_id = time.time()
    database.create_new_user(adapter_id)
    result = database.find_by_adapter_id(adapter_id)
    assert result is not None
    assert result.adapter_id == adapter_id


def test_updating_user():
    adapter_id = time.time()
    result = database.find_by_adapter_id(adapter_id)
    result.data['test_property'] = 'Hello, world'
    result.update()
    result = database.find_by_adapter_id(adapter_id)
    assert result.data['test_property'] == 'Hello, world'
