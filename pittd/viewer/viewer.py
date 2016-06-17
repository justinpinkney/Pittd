from flask import Flask, render_template

app = Flask(__name__)

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


@app.route('/')
def hello_world():
    return render_template('show_entries.html', entries=fake_data)


if __name__ == '__main__':
    app.run()
