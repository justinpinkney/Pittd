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

fake_data = [
    {
        'date': '2016 02 04',
        'content': [test_message, test_photo]
    },

    {
        'date': '2016 02 06',
        'content': [test_photo, test_message, test_message]
    }
]

"""


class Parser(object):
    def __init__(self, photo_directory, record_file):
        self.photo_directory = photo_directory
        self.record_file = record_file

    def update(self):
        self.parse_text()
        self.parse_photo()
        # Combine the lists and sort by date
        pass

    def parse_text(self, record_file):
        # For each line in the file, extract a message object, append to list
        pass

    def parse_photo(self, photo_directory):
        # For each photo in directory, extract message object, append to list
        pass


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

    def __init__(self, type, time, user, content):
        self.type = type
        self.time = time
        self.user = user
        self.content = content


class TextPost(Post):
    def __init__(self):
        super(TextPost, self).__init__()

    @classmethod
    def from_file(self, input_string):
        # "1970 Jan 01, 00-00-00 - Test person - message_body\n"
        post_date, remainder = input_string.split(',', 1).strip()
        post_time, remainder = remainder.split(' - ', 1).strip()
        post_user, post_content = remainder.split(' - ', 1).strip(' \n')
        return TextPost('text',
                        post_date,
                        post_time,
                        post_user,
                        post_content)


class PhotoPost(Post):
    def __init__(self):
        super(PhotoPost, self).__init__()

    @classmethod
    def from_file(self):
        pass
