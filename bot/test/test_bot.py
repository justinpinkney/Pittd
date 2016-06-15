import os
from datetime import datetime
from bot import telegram_bot
import telebot

TEST_LOG_FILE = 'test_log.txt'


def setup_function(function):
    """ Write to test file, fail if file already exists
    """
    telegram_bot.RECORD_FILE = TEST_LOG_FILE
    assert not os.path.isfile(TEST_LOG_FILE)


def teardown_function(function):
    """ Remove my test log file
    """
    if os.path.isfile(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)


def test_process_text():
    """ Test that a text message is correctly written to file.
    """
    expected_string = "1970 Jan 01, 00-00-00 - Test person - message_body\n"
    date_zero = 0

    params = {'text': 'message_body'}
    fake_message = telebot.types.Message(None, None,
                                         date_zero, None,
                                         'text',
                                         params)
    metadata = {
        'datetime': datetime.fromtimestamp(0),
        'user': 'Test person',
    }

    telegram_bot.process_text(fake_message, metadata)
    with open(telegram_bot.RECORD_FILE, 'r') as record_file:
        assert (record_file.readline() == expected_string)

# test process_photo - fake message, check written to file
# test generate photo path - check correct format
# test download file - download file from url, check saved, check bad url
# test extract metadata - make message, get data
