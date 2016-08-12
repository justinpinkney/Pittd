import logging
import sys
import traceback
import configparser
from datetime import datetime
from time import sleep
import telebot
from requests.exceptions import ReadTimeout

from pittd import posts
# Load config options
config = configparser.ConfigParser()
config.read(['pittd/config.ini', 'pittd/user_config.ini'])


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

my_bot = telebot.TeleBot(config['bot']['TOKEN'])
TIMEOUT = 100
SLEEP_TIME = 5


@my_bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    my_bot.reply_to(message, "Hello there!")


@my_bot.message_handler(content_types=['text', 'photo'])
def process(message):
    if message.from_user.id in config['bot']['ALLOWED_USERS']:
        if message.content_type == 'text':
            process_text(message)
        elif message.content_type == 'photo':
            process_photo(message)
    else:
        print('{} is not a valid user id.'.format(message.from_user.id))
        my_bot.reply_to(message,
                        "Sorry {}, I'm not allowed to talk to you".format(
                            message.from_user.id))


def process_text(message):
    this_post = posts.TextPost(datetime.fromtimestamp(message.date),
                               message.from_user.first_name,
                               message.text)
    this_post.to_file(config['log']['RECORD_FILE'])


def process_photo(message):
    this_post = posts.PhotoPost.from_url(datetime.fromtimestamp(message.date),
                                            message.from_user.first_name)
    this_post.download(config['log']['RECORD_DIRECTORY'], get_photo_url(message))


def get_photo_url(message):
    photo_file = my_bot.get_file(message.photo[-1].file_id).file_path
    return 'https://api.telegram.org/file/bot{}/{}'.format(my_bot.token,
                                                           photo_file)


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
            print(traceback.print_exc())
            print("Restarting the bot...")


if __name__ == '__main__':
    run()
