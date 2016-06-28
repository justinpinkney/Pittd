from flask import Flask, render_template, send_from_directory
from pittd.viewer.parser import Parser
from pittd.config import RECORD_DIRECTORY, RECORD_FILE

app = Flask(__name__)
parser = Parser(RECORD_DIRECTORY, RECORD_FILE)

@app.route('/')
def hello_world():
    return render_template('show_entries.html', entries=parser.data)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(RECORD_DIRECTORY,
                               filename, as_attachment=True)

@app.route('/update')
def update():
    parser.update()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
