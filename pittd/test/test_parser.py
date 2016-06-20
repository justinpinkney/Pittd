from datetime import datetime

from pittd.viewer import parser

TEST_LOG_FILE = 'pittd/test/data/log.txt'
TEST_BAD_LOG_FILE = 'pittd/test/data/bad_log.txt'
TEST_DATA_DIRECTORY = 'pittd/test/data'


def test_parse_photo_directory():
    pass


def test_text_log():
    text_list = parser.parse_text_log(TEST_LOG_FILE)
    assert len(text_list) is 2
    validate_post(text_list[0],
                  'text',
                  datetime(1970, 1, 1),
                  'Test person 1',
                  'message_body 1')
    validate_post(text_list[1],
                  'text',
                  datetime(1980, 1, 1),
                  'Test person 2',
                  'message_body 2 - followed by some more text')


def test_bad_text_log():
    text_list = parser.parse_text_log(TEST_BAD_LOG_FILE)
    assert len(text_list) is 0


def test_photo():
    photo_list = parser.parse_photo_directory(TEST_DATA_DIRECTORY)
    assert len(photo_list) is 2
    validate_post(photo_list[0],
                  'photo',
                  datetime(1970, 1, 1),
                  'Test person 1',
                  '1970 Jan 01, 00-00-00 - Test person 1.jpg')

    validate_post(photo_list[1],
              'photo',
              datetime(1980, 1, 1),
              'Test person 2',
              '1980 Jan 01, 00-00-00 - Test person 2.jpg')


def validate_post(post, type, time, user, content):
    assert post.post_type == type
    assert post.post_time == time
    assert post.user == user
    assert post.content == content
