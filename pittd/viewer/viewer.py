from flask import Flask, render_template, send_from_directory
from pittd.viewer.parser import Parser

FOLDER = '../test/data'

app = Flask(__name__)
parser = Parser('../test/data', '../test/data/log.txt')

@app.route('/')
def hello_world():
    return render_template('show_entries.html', entries=parser.data)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(FOLDER,
                               filename, as_attachment=True)


if __name__ == '__main__':
    app.run()