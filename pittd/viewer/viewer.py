from collections import OrderedDict
from itertools import islice
import configparser
from flask import Flask, render_template, send_from_directory, redirect, url_for
from pittd.viewer.parser import Parser
# Load config options
config = configparser.ConfigParser()
config.read(['pittd/config.ini', 'pittd/user_config.ini'])


app = Flask(__name__)
parser = Parser(config['log']['RECORD_DIRECTORY'], config['log']['RECORD_FILE'])


def paginate(ordered_dict, current_page, per_page):
    """Return a subset of an ordered dict for pagination."""
    total_posts = len(ordered_dict)
    if current_page * per_page > total_posts:
        # TODO throw an error
        return {}, False, False

    has_prev = current_page > 0
    has_next = (current_page + 1) * per_page < total_posts

    if has_next:
        return (OrderedDict(islice(ordered_dict.items(),
                                   current_page * per_page,
                                   (current_page + 1) * per_page)),
                has_next,
                has_prev)
    else:
        return (OrderedDict(islice(ordered_dict.items(),
                                   current_page * per_page,
                                   None)),
                has_next,
                has_prev)


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=0):
    [entries_to_display, has_next, has_prev] = paginate(parser.data, page,
                                                        config['log'][
                                                            'POSTS_PER_PAGE'])
    return render_template('show_entries.html',
                           entries=entries_to_display,
                           curr_page=page,
                           has_next=has_next,
                           has_prev=has_prev)


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(config['log']['RECORD_DIRECTORY'],
                               filename, as_attachment=True)


@app.route('/update')
def update():
    parser.update()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
