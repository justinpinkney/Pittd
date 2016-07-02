"""
At scheduled times run the parser.
Walk through all photos in directory structure, and all lines of text log.
Return a list of days:

test_message = {'type': 'text',
                'time': '08-03-34',
                'user': 'Justin',
                'message': 'Hello, this is Justin speaking.'}

test_photo = {'type': 'photo',
              'time': '08-09-34',
              'user': 'Ciara',
              'path': 'static/test_image.jpg'}

fake_data = {
    '2016 02 04': [test_message, test_photo],
    '2016 02 06': [test_photo, test_message, test_message]
}

"""
import os
from collections import OrderedDict

from pittd.posts import PhotoPost, TextPost


def parse_photo_directory(photo_directory):
    # For each photo in directory, extract message object, append to list
    photo_list =[]
    for dirpath, dirnames, filenames in os.walk(photo_directory):
        for filename in filenames:
            this_photo = os.path.join(dirpath, filename)
            this_photo = os.path.relpath(this_photo, photo_directory)
            photo_post = PhotoPost.from_file(this_photo)
            if photo_post:
                photo_list.append(photo_post)
            else:
                print("Could not load photo {}".format(this_photo))
    return photo_list


def parse_text_log(record_file):
    # For each line in the file, extract a message object, append to list
    text_list = []
    with open(record_file, 'r', encoding='utf-8') as text_log:
        for line in text_log.readlines():
            text_post = TextPost.from_file(line)
            if text_post:
                text_list.append(text_post)
            else:
                print("Could not load text {}".format(line))
    return text_list


def add_posts(data, posts):
    for post in posts:
        post_time = post.post_time.date()
        if post_time in data.keys():
            data[post_time].append(post)
            data[post_time].sort(key=lambda x: x.post_time)
        else:
            data[post_time] = [post,]


class Parser(object):
    def __init__(self, photo_directory, record_file):
        self.photo_directory = photo_directory
        self.record_file = record_file
        self.data = {}
        self.update()

    def update(self):
        text_list = parse_text_log(self.record_file)
        photo_list = parse_photo_directory(self.photo_directory)
        # Combine the lists, sort by date and make final structure
        add_posts(self.data, text_list)
        add_posts(self.data, photo_list)
        # Sort by date
        self.data = OrderedDict(sorted(self.data.items(), key=lambda x: x[0]))

