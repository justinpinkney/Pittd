import os
import shutil
from pittd.bot import telegram_bot
from telebot import types
from unittest.mock import patch

TEST_LOG_FILE = 'test_log_file.txt'
TEST_DATA_DIRECTORY = 'temp_directory'


def setup_function(function):
    """ Write to test file, fail if file already exists
    """
    telegram_bot.ALLOWED_USERS = (1,)
    telegram_bot.RECORD_FILE = TEST_LOG_FILE
    telegram_bot.RECORD_DIRECTORY = TEST_DATA_DIRECTORY
    assert not os.path.isfile(TEST_LOG_FILE)
    assert not os.path.exists(TEST_DATA_DIRECTORY)


def teardown_function(function):
    """ Remove my test log file
    """
    if os.path.isfile(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    if os.path.exists(TEST_DATA_DIRECTORY):
        shutil.rmtree(TEST_DATA_DIRECTORY)


def test_invalid_user():
    post_date = 0
    user_id = 0
    params = {'text': 'message_body'}
    user = types.User(user_id, 'Test person')
    # Stub out the reply_to call as we don't want to access the Telegram API
    telegram_bot.my_bot.reply_to = lambda x, y: print(x, y)
    text_message = types.Message(1, user, post_date, user, 'text', params)
    telegram_bot.process(text_message)

    assert not os.path.isfile(TEST_LOG_FILE)


def test_process_text_message():
    post_date = 0
    user_id = 1
    params = {'text': 'message_body'}
    user = types.User(user_id, 'Test person')
    text_message = types.Message(1, user, post_date, user, 'text', params)
    telegram_bot.process(text_message)

    assert os.path.isfile(TEST_LOG_FILE)


def test_process_photo_message():
    photo_url = '''https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Snow_Monkeys%2C_Nagano%2C_Japan.JPG/320px-Snow_Monkeys%2C_Nagano%2C_Japan.JPG'''
    # Stub out the get_photo_url call as we don't want to access the Telegram API
    post_date = 0
    user_id = 1
    params = {'photo': 'message_body'}
    user = types.User(user_id, 'Test person')
    photo_message = types.Message(1, user, post_date, user, 'photo', params)
    telegram_bot.get_photo_url = lambda x: photo_url
    telegram_bot.process(photo_message)

    assert os.path.exists(TEST_DATA_DIRECTORY)
