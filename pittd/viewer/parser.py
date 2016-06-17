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


