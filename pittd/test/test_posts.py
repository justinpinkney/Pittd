import os
from datetime import datetime
import shutil
from pittd import posts

TEST_LOG_FILE = 'test_log_file.txt'
TEST_DATA_DIRECTORY = 'temp_directory'


def setup_function(function):
    """ Write to test file, fail if file already exists
    """
    assert not os.path.isfile(TEST_LOG_FILE)
    assert not os.path.exists(TEST_DATA_DIRECTORY)


def teardown_function(function):
    """ Remove my test log file
    """
    if os.path.isfile(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    if os.path.exists(TEST_DATA_DIRECTORY):
        shutil.rmtree(TEST_DATA_DIRECTORY)


def test_text_post_to_file():
    test_time = datetime.fromtimestamp(0)
    user = 'Test person'
    content = 'message_body'
    expected_string = "1970 Jan 01, 00-00-00 - Test person - message_body\n"

    this_post = posts.TextPost(test_time, user, content)
    this_post.to_file(TEST_LOG_FILE)

    with open(TEST_LOG_FILE, 'r') as record_file:
        assert record_file.readline() == expected_string


def test_text_post_from_file():
    test_string = "1970 Jan 01, 00-00-00 - Test person - message_body\n"
    test_time = datetime.fromtimestamp(0)
    user = 'Test person'
    content = 'message_body'

    this_post = posts.TextPost.from_file(test_string)
    assert this_post.post_time == test_time
    assert this_post.user == user
    assert this_post.content == content


def test_photo_post():
    expected_string = os.path.join("1970-01",
                                   "1970 Jan 01, 00-00-00 - Test person.jpg")
    test_time = datetime.fromtimestamp(0)
    user = 'Test person'
    this_post = posts.PhotoPost(test_time, user)

    assert this_post.post_time == test_time
    assert this_post.user == user
    assert this_post.content == expected_string


def test_photo_post_to_file():
    photo_url = '''https://upload.wikimedia.org/wikipedia/commons/6/61/Snow_Monkeys%2C_Nagano%2C_Japan.JPG'''
    test_time = datetime.fromtimestamp(0)
    user = 'Test person'
    this_post = posts.PhotoPost(test_time, user)
    this_post.to_file(TEST_DATA_DIRECTORY, photo_url)

    assert os.path.isfile(os.path.join(TEST_DATA_DIRECTORY, this_post.content))


def test_photo_post_from_file():
    pass
