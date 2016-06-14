import shutil
import os
from time import sleep

import requests
import telebot
import logging
import sys
from datetime import datetime

from requests.exceptions import ReadTimeout

from bot.config import ALLOWED_USERS, TOKEN, record_directory, record_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

date_format = '%Y %b %d, %H-%M-%S'
my_bot = telebot.TeleBot(TOKEN)
TIMEOUT = 100


@my_bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    my_bot.reply_to(message, "hello there!")


@my_bot.message_handler(content_types=['text', 'photo'])
def process(message):
    if validated_user(message.from_user.id):
        metadata = extract_metadata(message)
        if message.content_type == 'text':
            process_text(message, metadata)
        elif message.content_type == 'photo':
            process_photo(message, metadata)
    else:
        my_bot.reply_to(message,
                        "Sorry {}, I'm not allowed to talk to you").format(
            message.from_user.id)


def process_text(message, metadata):
    with open(record_file, 'a', encoding='utf-8') as f:
        time_string = metadata['datetime'].strftime(date_format)
        for line in message.text.split('\n'):
            f.write(
                '{} - {} - {}\n'.format(time_string, metadata['user'], line))


def process_photo(message, metadata):
    folder = os.path.join(record_directory,
                          metadata['datetime'].strftime('%Y-%m'))
    time_string = metadata['datetime'].strftime(date_format)
    file_name = '{} - {}.jpg'.format(time_string, metadata['user'])

    if not os.path.exists(folder):
        os.makedirs(folder)

    download_file(os.path.join(folder, file_name), get_photo_url(message))


def get_photo_url(message):
    photo_file = my_bot.get_file(message.photo[-1].file_id).file_path
    return 'https://api.telegram.org/file/bot{}/{}'.format(TOKEN, photo_file)


def download_file(save_location, url):
    """Download an file to disk."""
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_location, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise IOError("Could not download file.")


def extract_metadata(message):
    metadata = {
        'datetime': datetime.fromtimestamp(message.date),
        'user': message.from_user.first_name,
    }
    return metadata


def validated_user(user_id):
    if user_id in ALLOWED_USERS:
        return True
    else:
        print('{} is not a valid user id.'.format(user_id))
        return False


def run():
    while True:
        sleep(1)
        try:
            my_bot.polling(timeout=TIMEOUT)
        except ReadTimeout as e:
            print("Got a timeout error, restarting the bot...")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Restarting the bot...")


if __name__ == '__main__' \
               '':
    run()
