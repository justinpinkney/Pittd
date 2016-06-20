import os
from datetime import datetime

import requests
import shutil


class Post(object):
    """
    Could implement to_file and from_message methods and use these throughout.
    test_message = {'type': 'text',
                    'time': '08-03-34',
                    'user': 'Justin',
                    'content': 'Hello, this is Justin speaking.'}

    test_photo = {'type': 'photo',
                  'time': '08-09-34',
                  'user': 'Ciara',
                  'content': 'static/test_image.jpg'}
    """

    date_format = '%Y %b %d, %H-%M-%S'
    month_format = '%Y-%m'
    delim = ' - '

    def __init__(self, post_type, post_time, user, content):
        self.post_type = post_type
        self.post_time = post_time
        self.user = user
        self.content = content


class TextPost(Post):
    def __init__(self, time, user, content):
        super(TextPost, self).__init__('text', time, user, content)

    @classmethod
    def from_file(cls, input_string):
        # "1970 Jan 01, 00-00-00 - Test person - message_body\n"
        try:
            datetime_string, remainder = input_string.split(Post.delim, 1)
            post_time = datetime.strptime(datetime_string, Post.date_format)
            post_user, post_content = remainder.split(Post.delim, 1)
        except ValueError:
            return None
        return TextPost(post_time, post_user, post_content.strip('\n'))

    def to_file(self, destination_file):
        with open(destination_file, 'a', encoding='utf-8') as f:
            time_string = self.post_time.strftime(self.date_format)
            for line in self.content.split('\n'):
                f.write(
                    Post.delim.join(('{}', '{}', '{}\n'))
                        .format(time_string, self.user, line))


class PhotoPost(Post):
    def __init__(self, time, user, content):
        super(PhotoPost, self).__init__('photo', time, user, content)


    @classmethod
    def from_url(cls, time, user):

        folder = os.path.join(time.strftime(Post.month_format))
        time_string = time.strftime(Post.date_format)
        file_name = Post.delim.join(('{}', '{}.jpg')).format(time_string, user)
        content = os.path.join(folder, file_name)
        return PhotoPost(time, user, content)

    @classmethod
    def from_file(cls, path):
        # Check the filename format
        root, filename = os.path.split(path)
        this_post = cls.parse_photo_name(filename)
        if not this_post:
            this_post = cls.parse_photo_metadata(filename)
        return this_post


    @classmethod
    def parse_photo_name(cls, filename):
        try:
            datetime_string, user = filename.split(Post.delim, 1)
            post_time = datetime.strptime(datetime_string, Post.date_format)
            user = user.strip('.jpg')
            return PhotoPost(post_time, user, filename)
        except ValueError:
            # The filename is not the correct format
            return None

    def download(self, record_directory, url):
        folder = os.path.join(record_directory, os.path.split(self.content)[0])
        if not os.path.exists(folder):
            os.makedirs(folder)

        download_file(os.path.join(record_directory, self.content), url)

    @classmethod
    def parse_photo_metadata(cls, filename):
        #TODO
        return None


def download_file(save_location, url):
    """Download an file to disk."""
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_location, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise IOError("Could not download file.")
