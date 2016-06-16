import shutil
import os
from time import sleep
import requests
import telebot
import logging
import sys
from datetime import datetime
from requests.exceptions import ReadTimeout

from bot.config import ALLOWED_USERS, TOKEN, RECORD_DIRECTORY, RECORD_FILE

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

date_format = '%Y %b %d, %H-%M-%S'
my_bot = telebot.TeleBot(TOKEN)
TIMEOUT = 100
SLEEP_TIME = 1


@my_bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    my_bot.reply_to(message, "Hello there!")


@my_bot.message_handler(content_types=['text', 'photo'])
def process(message):
    if message.from_user.id in ALLOWED_USERS:
        metadata = extract_metadata(message)
        if message.content_type == 'text':
            process_text(message, metadata)
        elif message.content_type == 'photo':
            process_photo(message, metadata)
    else:
        print('{} is not a valid user id.'.format(message.from_user.id))
        my_bot.reply_to(message,
                        "Sorry {}, I'm not allowed to talk to you".format(
                            message.from_user.id))


def process_text(message, metadata):
    with open(RECORD_FILE, 'a', encoding='utf-8') as f:
        time_string = metadata['datetime'].strftime(date_format)
        for line in message.text.split('\n'):
            f.write(
                '{} - {} - {}\n'.format(time_string, metadata['user'], line))


def process_photo(message, metadata):
    download_file(generate_photo_path(RECORD_DIRECTORY,
                                      metadata['datetime'],
                                      metadata['user']),
                  get_photo_url(message))


def generate_photo_path(directory, photo_datetime, user):
    folder = os.path.join(directory,
                          photo_datetime.strftime('%Y-%m'))
    time_string = photo_datetime.strftime(date_format)
    file_name = '{} - {}.jpg'.format(time_string, user)

    if not os.path.exists(folder):
        os.makedirs(folder)

    return os.path.join(folder, file_name)


def get_photo_url(message):
    photo_file = my_bot.get_file(message.photo[-1].file_id).file_path
    return 'https://api.telegram.org/file/bot{}/{}'.format(my_bot.token,
                                                           photo_file)


def download_file(save_location, url):
    """Download an file to disk."""
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_location, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise IOError("Could not download file.")


def extract_metadata(message):
    """Extract the date and user from a message."""
    metadata = {
        'datetime': datetime.fromtimestamp(message.date),
        'user': message.from_user.first_name,
    }
    return metadata


def run():
    """Run the Bot."""
    while True:
        sleep(SLEEP_TIME)
        try:
            my_bot.polling(timeout=TIMEOUT)
        except ReadTimeout as e:
            print("Got a timeout error, restarting the bot...")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Restarting the bot...")


if __name__ == '__main__':
    run()
